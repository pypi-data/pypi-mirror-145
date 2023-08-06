from typing import List, Dict, Tuple
from itertools import islice
from collections import Counter
import logging

import numpy as np

import cactice.grids
from cactice.grids import get_neighborhood, get_neighborhoods, Neighbors
from cactice.distance import hamming_distance


class KNN:
    def __init__(
            self,
            k: int = 10,
            neighbors: Neighbors = Neighbors.CARDINAL):
        """
        Create a K-nearest neighbors model.

        :param neighbors: Which adjacent cells to consider neighbors.
        """

        self.__logger = logging.getLogger(__name__)
        self.__fit: bool = False
        self.__k: int = k
        self.__neighbors: Neighbors = neighbors
        self.__train: List[np.ndarray] = []
        self.__cell_distribution: Dict[str, float] = {}

        # store neighborhoods as a list of grids,
        # each grid a dictionary mapping absolute cell coordinates (i, j) to neighborhoods,
        # each neighborhood a dictionary mapping relative cell coordinates (i, j) to values
        self.__neighborhoods: List[Dict[Tuple[int, int], Dict[Tuple[int, int], int]]] = []

    def fit(self, grids: List[np.ndarray]):
        """
        Fit the model to the given grids.
        """

        self.__train = grids
        self.__cell_distribution = cactice.grids.cell_value_distribution(grids, exclude_zero=True)

        # for each grid...
        for grid in grids:
            # create dictionary mapping cell location to neighborhood
            neighborhoods = get_neighborhoods(grid, self.__neighbors, include_center=True, exclude_zero=True)
            self.__neighborhoods.append(neighborhoods)

        self.__fit = True

    def predict(self, grids: List[np.ndarray] = None) -> List[np.ndarray]:
        """
        Predict missing cells on the training grids or on the given grids (if provided).
        To generate entirely novel grids conditioned on the training set, provide a list of empty (zero-valued) arrays.

        :param grids: The grids to predict on (if none are provided the training set will be used).
        :return: The predicted grids.
        """

        if not self.__fit:
            raise ValueError(f"Model must be fit before predictions can be made!")

        # initialize grids to predict on
        grid_predictions = [np.copy(grid) for grid in (grids if grids is not None else self.__train)]

        # flatten all training grids' neighborhoods into one list
        neighborhoods = [h for hs in [list(nhds.values()) for nhds in self.__neighborhoods] for h in hs]

        for gi, grid in enumerate(grid_predictions):
            # find cells to predict (missing locations)
            rows = range(0, grid.shape[0])
            cols = range(0, grid.shape[1])
            grid_pred = grid_predictions[gi].copy()
            missing = [(i, j) for i in rows for j in cols if grid_pred[i, j] == 0]

            # if this grid has no missing locations, skip it
            if len(missing) == 0: continue

            # predict cells one by one
            for i, j in missing:
                # get the missing location's neighbors
                neighborhood = get_neighborhood(
                    grid=grid,
                    i=i,
                    j=j,
                    neighbors=self.__neighbors,
                    include_center=False,
                    exclude_zero=True)

                # pull out neighbor cell values
                neighbors = list(neighborhood.values())

                if len(neighbors) > 0:
                    self.__logger.debug(f"Assigning location ({i}, {j}) via KNN")

                    # compute distance from this neighborhood to every training neighborhood
                    distances = {nh[(0, 0)]: hamming_distance(neighbors, [v for k, v in nh.items() if k != (0, 0)]) for nh in neighborhoods}

                    # sort distances ascending
                    distances = dict(sorted(distances.items(), key=lambda k, v: v, reverse=True))

                    # keep k most similar neighborhoods (k nearest neighbor neighborhoods)
                    distances = dict(islice(distances, self.__k))

                    # count frequency of each cell value in and pick the most common (ties broken randomly)
                    cell_pred = Counter(distances.values()).most_common(1)[0][0]
                else:
                    self.__logger.debug(
                        f"Location ({i}, {j}) has no neighbors, assigning by sampling from cell distribution")

                    # sample randomly according to cell class distribution
                    cell_pred = np.random.choice(
                        a=list(self.__cell_distribution.keys()),
                        p=list(self.__cell_distribution.values()))

                # set the cell in the corresponding grid
                grid_pred[i, j] = cell_pred

            # set the predicted grid
            grid_predictions[gi] = grid_pred

        return grid_predictions
