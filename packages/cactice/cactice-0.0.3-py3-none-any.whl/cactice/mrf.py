import collections
import random
from itertools import product
from typing import List, Tuple, Callable, Dict, OrderedDict
import logging

import numpy as np
from numpy.random import choice, RandomState

import cactice.grids
from cactice.grids import Neighbors, get_neighborhood, get_neighborhoods

# bond interaction signature
# params:
#  - grid
#  - location A
#  - location B
# returns: bond energy
Interaction = Callable[[np.ndarray, Tuple[int, int], Tuple[int, int]], float]


def bond_energies(
        grid: np.ndarray,
        neighbors: Neighbors,
        interaction: Interaction) -> Dict[Tuple[Tuple[int, int], Tuple[int, int]], float]:
    """
    Computes bonds and bond energies for the given grid and interaction function.

    TODO: allow neighbor specification (cardinal, diagonal, complete)

    :param grid: The grid
    :param interaction: The interaction function
    :return: A dictionary mapping bonds to bond energies
    """

    bonds = dict()
    h, w = grid.shape

    # horizontal interactions
    for i, j in product(range(h - 1), range(w)):
        e = interaction(grid, (i, j), (i + 1, j))
        bonds[((i, j), (i + 1, j))] = e

    # vertical interactions
    for i, j in product(range(h), range(w - 1)):
        e = interaction(grid, (i, j), (i, j + 1))
        bonds[((i, j), (i, j + 1))] = e

    return bonds


def H(grid: np.ndarray,
      neighbors: Neighbors,
      interaction: Interaction,
      J: float = 1.0) -> float:
    """
    Computes the Hamiltonian (energy function) of the given grid

    :param grid: The grid
    :param interaction: The bond interaction
    :param J: The multiplier
    :return: The energy
    """
    bonds = bond_energies(grid, neighbors, interaction)
    e = sum(bonds.values())
    return J * e


def neighborhood_H(
        grid: np.ndarray,
        cell: Tuple[int, int],
        neighbors: Neighbors,
        interaction: Interaction,
        J: float = 1.0) -> float:
    """
    Computes the Hamiltonian (energy function) of the given neighborhood.

    :param grid: The grid
    :param cell: The cell around which the neighborhood is centered
    :param interaction: The bond interaction
    :param J: The multiplier
    :return: The energy
    """

    i, j = cell
    e = 0

    neighborhood = get_neighborhood(
        grid=grid,
        i=i,
        j=j,
        neighbors=neighbors,
        include_center=False,
        exclude_zero=True)

    for (ni, nj), nv in neighborhood.items():
        e += interaction(grid, (i + ni, j + nj), (i, j))

    # if i > 0: e += interaction(grid, (i - 1, j), (i, j))
    # if i < w - 1: e += interaction(grid, (i, j), (i + 1, j))
    # if j > 0: e += interaction(grid, (i, j - 1), (i, j))
    # if j < h - 1: e += interaction(grid, (i, j), (i, j + 1))

    return J * e


class MRF:
    def __init__(
            self,
            neighbors: Neighbors = Neighbors.CARDINAL,
            interaction: str = 'proportional',
            # interaction: Interaction,
            J: float = 1.0,
            iterations: int = 250,
            threshold: float = 0.01,
            seed: int = 42):
        """
        Create a Markov random field model.

        :param neighbors: Which cells to consider part of each cell's neighborhood
        :param interaction: The bond interaction ('proportional' or 'kronecker')
        :param J: The multiplier
        :param iterations: The number of iterations of the Metropolis algorithm to run
        :param threshold: The probability of accepting a detrimental update
        :param seed: The random seed
        """

        self.__logger = logging.getLogger(__name__)
        self.__fit: bool = False
        self.__random_state: RandomState = RandomState(seed)
        self.__neighbors: Neighbors = neighbors
        self.__interaction: str = interaction
        # self.__interaction: Interaction = interaction
        self.__J: float = J
        self.__iterations: int = iterations
        self.__threshold: float = threshold
        self.__train: List[np.ndarray] = []
        self.__cell_distribution: Dict[int, float] = {}
        self.__bond_distribution_horiz: Dict[Tuple[int, int], float] = {}
        self.__bond_distribution_vert: Dict[Tuple[int, int], float] = {}

        # store neighborhoods as a list of grids,
        # each grid a dictionary mapping absolute cell coordinates (i, j) to neighborhoods,
        # each neighborhood a dictionary mapping relative cell coordinates (i, j) to values
        self.__neighborhoods: List[Dict[Tuple[int, int], Dict[Tuple[int, int], int]]] = []

    def __kronecker_interaction(
            self,
            grid: np.ndarray,
            p1: Tuple[int, int],
            p2: Tuple[int, int]) -> float:
        """
        Yields an interaction energy of 1 if the cells have the same class, otherwise 0.

        :param grid: The grid
        :param p1: The first cell location
        :param p2: The second cell location
        :return:
        """

        (i1, j1) = p1
        (i2, j2) = p2
        if abs(i1 - i2) > 1 or abs(j1 - j2) > 1:
            raise ValueError(
                f"Only immediately adjacent neighbors (in the 4 cardinal and 4 diagonal directions) are supported")

        # TODO: check neighbor strategy and depth

        v1 = int(grid[i1, j1])
        v2 = int(grid[i2, j2])

        if v1 == 0 or v2 == 0 or v1 != v2: return 0
        else: return 1

    def __proportional_interaction(
            self,
            grid: np.ndarray,
            p1: Tuple[int, int],
            p2: Tuple[int, int]) -> float:
        """
        Interprets adjacency probability mass as interaction energy.
        Really just a lookup table on the bond distribution.

        :param grid: The grid
        :param p1: The first cell location
        :param p2: The second cell location
        :return: The interaction energy
        """

        (i1, j1) = p1
        (i2, j2) = p2
        if abs(i1 - i2) > 1 or abs(j1 - j2) > 1:
            raise ValueError(
                f"Only immediately adjacent neighbors (in the 4 cardinal and 4 diagonal directions) are supported")

        # TODO: check neighbor strategy and depth

        v1 = int(grid[i1, j1])
        v2 = int(grid[i2, j2])
        sk = sorted([v1, v2])
        key = (sk[0], sk[1])

        if v1 == 0 or v2 == 0: return 0
        elif i1 == i2: return self.__bond_distribution_vert[key]
        elif j1 == j2: return self.__bond_distribution_horiz[key]

    def fit(self, grids: List[np.ndarray]):
        """
        Fit the model to the given grids (precompute neighborhoods and probability distribution).
        """

        self.__train = grids
        self.__cell_distribution = cactice.grids.cell_value_distribution(grids, exclude_zero=True)
        self.__bond_distribution_horiz, self.__bond_distribution_vert = cactice.grids.undirected_bond_distribution(
            grids=grids,
            exclude_zero=True)

        # for each grid...
        for grid in grids:
            # create dictionary mapping cell location to neighborhood
            neighborhoods = get_neighborhoods(grid, self.__neighbors, exclude_zero=True)
            self.__neighborhoods.append(neighborhoods)

        self.__fit = True

    def predict(self, grids: List[np.ndarray] = None) -> List[np.ndarray]:
        """
        Predict missing cells on the training grids or on the given grids (if provided).
        To generate entirely novel grids conditioned on the training set, provide a list of empty (zero-valued) arrays.
        This method uses the Metropolis algorithm to minimize the bond energy (roughly, "surprise") on the predicted grids, conditioned on the training grids' bond distribution.

        :param grids: The grids to predict on (the training set will be used otherwise)
        :return: The grids with missing values filled in.
        """

        if not self.__fit:
            raise ValueError(f"Model must be fit before predictions can be made!")

        # initialize grids to predict on
        grid_predictions = [np.copy(grid) for grid in (grids if grids is not None else self.__train)]

        for gi, grid in enumerate(grid_predictions):
            # find cells to predict (missing locations)
            h, w = grid.shape
            rows = range(0, h)
            cols = range(0, w)
            missing: List[Tuple[int, int]] = [(i, j) for i in rows for j in cols if grid[i, j] == 0]

            pred = np.copy(grid)
            accepted = 0
            rejected = 0
            total_energies = []
            average_energies = []
            updates: OrderedDict[Tuple[int, int], int] = collections.OrderedDict()

            # randomly initialize missing cells
            for i, j in missing: pred[i, j] = choice(list(self.__cell_distribution.keys()), 1)[0]

            # proceed while we haven't reached the cutoff point
            while accepted < self.__iterations and rejected < self.__iterations:
                # make a copy of the grid
                pcpy = np.copy(pred)

                # pick random missing location
                i, j = missing[random.randint(0, len(missing) - 1)]

                # make random selection from class distribution
                cell = choice(list(self.__cell_distribution.keys()), 1)[0]
                pcpy[i, j] = cell

                # compute the energy pre- and post-update and calculate difference
                if self.__interaction == 'proportional':
                    interaction: Interaction = self.__proportional_interaction
                elif self.__interaction == 'kronecker':
                    interaction: Interaction = self.__kronecker_interaction
                else:
                    raise ValueError(f"Unsupported interaction: {self.__interaction}")

                energy_old = neighborhood_H(pred, (i, j), self.__neighbors, interaction)
                energy_new = neighborhood_H(pcpy, (i, j), self.__neighbors, interaction)
                difference = energy_new - energy_old

                # compute the total and average energy corresponding to the new configuration
                values_ttl = len([p for p in np.ravel(grid) if p != 0])
                energy_ttl = H(np.vectorize(lambda x: float(x))(pcpy), self.__neighbors, interaction)
                energy_avg = (energy_ttl / values_ttl) if values_ttl > 0 else 0

                # if we lowered the energy (or random chance of detriment if we didn't), accept the update
                if difference < 0 or self.__random_state.uniform() > (1 - self.__threshold):
                    accepted += 1
                    total_energies.append(energy_ttl)
                    average_energies.append(energy_avg)
                    updates[(i, j)] = cell

                    # update predicted grid
                    pred[i, j] = cell
                else:
                    rejected += 1
                    if len(total_energies) > 0:
                        total_energies.append(total_energies[-1])
                        average_energies.append(average_energies[-1])

            # save predicted grid
            grid_predictions[gi] = pred

        return grid_predictions
