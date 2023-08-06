import logging
from collections import OrderedDict, Counter
from enum import Enum
from itertools import product, repeat
from typing import Dict, Tuple, List

import numpy as np

from cactice.distance import hamming_distance

logger = logging.getLogger(__name__)


class Neighbors(Enum):
    CARDINAL = 1  # top, bottom, left, right
    DIAGONAL = 2  # top left, top right, bottom left, bottom right
    COMPLETE = 3  # all the above
    HORIZONTAL = 4  # only left & right
    VERTICAL = 5  # only top & bottom


def flatten(grids: List[np.ndarray]) -> List[int]:
    """
    Flattens the given grids into a single list of cell values

    :param grids: The grids to flatten
    :return: The flattened list of grid cells
    """
    return [int(c) for cc in
            [r for row in [[grid[col_i] for col_i in range(0, grid.shape[0])] for grid in grids] for r in row] for
            c in cc]


def get_neighborhood(
        grid: np.ndarray,
        i: int,
        j: int,
        neighbors: Neighbors = Neighbors.CARDINAL,
        include_center: bool = False,
        exclude_zero: bool = False,
        absolute_coords: bool = False) -> Dict[Tuple[int, int], int]:
    """
    Gets the neighborhood around the given grid cell.

    :param grid: The grid
    :param i: The cell's row index
    :param j: The cell's column index
    :param neighbors: The cells to consider neighbors
    :param include_center: Whether to include the central cell in the neighborhood
    :param exclude_zero: Whether to exclude zero-valued neighbors
    :param absolute_coords: Use absolute coordinates rather than location relative to the central cell (the default)
    :return: A dictionary mapping cell locations to their respective values
    """

    # optionally include the central cell in the neighborhood we'll return
    neighborhood = {(0, 0): grid[i, j]} if include_center else {}

    irange = (max(i - 1, 0), min(i + 1, grid.shape[0]))
    jrange = (max(j - 1, 0), min(j + 1, grid.shape[1]))
    for ii in range(irange[0], irange[1] + 1):
        for jj in range(jrange[0], jrange[1] + 1):
            # ignore the center
            if i == ii and j == jj:
                continue

            # make sure we're still within the grid
            if ii >= grid.shape[0] or jj >= grid.shape[1]:
                continue

            # use relative or absolute coordinates
            coords = (ii, jj) if absolute_coords else (ii - i, jj - j)

            # diagonals: both coords are different
            if (neighbors == Neighbors.DIAGONAL or neighbors == Neighbors.COMPLETE) \
                    and (i != ii and j != jj):
                logger.info(f"Adding cell ({i}, {j})'s diagonal neighbor ({ii}, {jj})")
                neighborhood[coords] = grid[ii, jj]

            # cardinals: 1 coord equal, 1 different
            elif (neighbors == Neighbors.CARDINAL or neighbors == Neighbors.COMPLETE) \
                    and ((i == ii and j != jj) or (i != ii and j == jj)):
                logger.info(f"Adding cell ({i}, {j})'s cardinal neighbor ({ii}, {jj}), ({i}, {j})")
                neighborhood[coords] = grid[ii, jj]

            # horizontal: i equal, j different
            elif (neighbors == Neighbors.HORIZONTAL) and (i == ii and j != jj):
                logger.info(f"Adding cell ({i}, {j})'s horizontal neighbor ({ii}, {jj}), ({i}, {j})")
                neighborhood[coords] = grid[ii, jj]

            # vertical: i different, j equal
            elif (neighbors == Neighbors.VERTICAL) and (i != ii and j == jj):
                logger.info(f"Adding cell ({i}, {j})'s vertical neighbor ({ii}, {jj}), ({i}, {j})")
                neighborhood[coords] = grid[ii, jj]

    # optionally exclude zeros (interpreted as missing values)
    if exclude_zero:
        neighborhood = {k: v for k, v in neighborhood.items() if (k == (0, 0) or (k != (0, 0) and v != 0))}

    return neighborhood


def get_neighborhoods(
        grid: np.ndarray,
        neighbors: Neighbors = Neighbors.CARDINAL,
        include_center: bool = False,
        exclude_zero: bool = False,
        absolute_coords: bool = False):
    """
    Gets all cell neighborhoods in the given grid.

    :param grid: The grid
    :param neighbors: The cells to consider neighbors
    :param include_center: Whether to include the central cell in the neighborhood
    :param exclude_zero: Whether to exclude zero-valued neighbors
    :param absolute_coords: Use absolute coordinates rather than location relative to the central cell (the default)
    :return: A dictionary mapping cell locations to dictionaries mapping relative locations around the central cell to neighboring values
    """

    return {(i, j): get_neighborhood(grid=grid,
                                     i=i,
                                     j=j,
                                     neighbors=neighbors,
                                     include_center=include_center,
                                     exclude_zero=exclude_zero,
                                     absolute_coords=absolute_coords)
            for i in range(0, grid.shape[0])
            for j in range(0, grid.shape[1])}


def neighborhood_distribution(
        grid: np.ndarray,
        neighbors: Neighbors = Neighbors.CARDINAL,
        exclude_zero: bool = False) -> Dict[int, Dict[int, float]]:
    """

    :param grid:
    :param neighbors:
    :param exclude_zero:
    :return:
    """

    neighborhoods = get_neighborhoods(grid=grid, neighbors=neighbors, exclude_zero=exclude_zero, absolute_coords=True)
    unique = list(set(np.unique(np.ravel(grid))))
    if exclude_zero: unique = [c for c in unique if c != 0]
    freq = {k: {kk: 0 for kk in unique} for k in unique}
    for loc, neighborhood in neighborhoods.items():
        k = grid[loc[0], loc[1]]
        if exclude_zero and k == 0: continue
        for nloc, neighbor in neighborhood.items():
            nk = grid[nloc[0], nloc[1]]
            if exclude_zero and nk == 0: continue
            freq[k][nk] += 1

    return {k: {kk: (v[kk] / sum(freq[k].values())) for kk in unique} for (k, v) in freq.items()}


def get_band(
        grid: np.ndarray,
        i: int,
        j: int,
        radius: int = 1,
        include_center: bool = False,
        exclude_zero: bool = False,
        absolute_coords: bool = False) -> Dict[Tuple[int, int], int]:
    """
    Gets the (square) band at the given distance around the given cell location.

    :param grid: The grid
    :param i: The central cell's row index
    :param j: The central cell's column index
    :param radius: The distance from the central cell to the band
    :param include_center: Whether to include the central cell in the neighborhood
    :param exclude_zero: Whether to exclude zero-valued cells
    :param absolute_coords: Use absolute coordinates rather than location relative to the central cell (the default)
    :return: A dictionary mapping cell locations to their respective values
    """

    if radius < 1 or radius > min(grid.shape):
        raise ValueError(f"Band radius must be greater than 0 and less than min(grid length, grid width)")

    band = {(0, 0): grid[i, j]} if include_center else {}
    ir = (max(i - radius, 0), min(i + radius, grid.shape[0]))
    jr = (max(j - radius, 0), min(j + radius, grid.shape[1]))
    for ii in range(ir[0], ir[1] + 1):
        for jj in range(jr[0], jr[1] + 1):
            # skip interior cells
            if (ii != ir[0] and ii != ir[1]) and (jj != jr[0] and jj != jr[1]):
                continue

            # make sure we're still within the grid
            if ii >= grid.shape[0] or jj >= grid.shape[1]:
                continue

            # map the cell's value to relative or absolute coordinates
            logger.info(f"Adding cell ({i}, {j})'s band cell ({ii}, {jj})")
            coords = (ii, jj) if absolute_coords else (ii - i, jj - j)
            band[coords] = grid[ii, jj]

    # optionally exclude zeros (missing values)
    if exclude_zero:
        band = {k: v for k, v in band.items() if (k == (0, 0) or (k != (0, 0) and v != 0))}

    return band


def get_bands(
        grid: np.ndarray,
        radius: int = 1,
        include_center: bool = False,
        exclude_zero: bool = False,
        absolute_coords: bool = False) -> Dict[Tuple[int, int], int]:
    """
    Gets all bands at the given distance in the given grid.

    :param grid: The grid
    :param radius: The distance from the central cell to start the band
    :param include_center: Whether to include the central cell in the neighborhood
    :param exclude_zero: Whether to exclude zero-valued cells
    :param absolute_coords: Use absolute coordinates rather than location relative to the central cell (the default)
    :return: A dictionary mapping cell locations to dictionaries mapping band cell locations to their respective values
    """

    if radius < 1 or radius > min(grid.shape):
        raise ValueError(f"Band radius must be greater than 0 and less than min(grid length, grid width)")

    return {(i, j): get_band(grid=grid,
                             radius=radius,
                             i=i,
                             j=j,
                             include_center=include_center,
                             exclude_zero=exclude_zero,
                             absolute_coords=absolute_coords)
            for i in range(0, grid.shape[0])
            for j in range(0, grid.shape[1])}


def get_bin(
        grid: np.ndarray,
        i: int,
        j: int,
        d_min: float,
        d_max: float,
        include_center: bool = False,
        exclude_zero: bool = False,
        absolute_coords: bool = False) -> Dict[Tuple[int, int], int]:
    """
    Gets the cells within the given distance range from the given cell in the given grid.

    :param grid: The grid
    :param i: The central cell's row index
    :param j: The central cell's column index
    :param d_min: The bin's lower distance bound
    :param d_max: The bin's upper distance bound
    :param include_center: Whether to include the central cell in the neighborhood
    :param exclude_zero: Whether to exclude zero-valued cells
    :param absolute_coords: Use absolute coordinates rather than location relative to the central cell (the default)
    :return: A dictionary mapping cell locations to dictionaries mapping band cell locations to their respective values
    """

    if d_min < 1 or d_min > min(grid.shape):
        raise ValueError(f"Bin distance lower bound must be greater than 0 and less than min(grid length, grid width)")

    if d_max < 1 or d_max > min(grid.shape):
        raise ValueError(f"Bin distance upper bound must be greater than 0 and less than min(grid length, grid width)")

    if d_min >= d_max:
        raise ValueError(f"Bin distance lower bound must be strictly less than upper bound")

    distances = {(ii, jj): np.linalg.norm(np.array((i, j)) - np.array((ii, jj)))
                 for ii in range(0, grid.shape[0])
                 for jj in range(0, grid.shape[1])}
    binn = {(0, 0): grid[i, j]} if include_center else {}  # don't shadow built-in `bin`
    for loc, distance in distances.items():
        if distance < d_min or distance > d_max: continue

        # map the cell's value to relative or absolute coordinates
        ii, jj = loc
        logger.info(f"Adding cell ({i}, {j})'s band cell ({ii}, {jj})")
        coords = (ii, jj) if absolute_coords else (ii - i, jj - j)
        binn[coords] = grid[ii, jj]

    # optionally exclude zeros (missing values)
    if exclude_zero:
        binn = {k: v for k, v in binn.items() if (k == (0, 0) or (k != (0, 0) and v != 0))}

    return binn


def neighborhood_correlations(
        grid: np.ndarray,
        radius: int = 1,
        exclude_zero: bool = False) -> Tuple[Dict[Tuple[int, int], float], np.ndarray]:
    """
    Computes the mean Hamming distance between each cell's neighborhood and those of all cells at distance `d` from it.

    :param grid: The grid
    :param radius: The radius of the band with reference to the central cell
    :param exclude_zero: Whether to exclude zero-valued cells
    :return: A tuple (dictionary mapping location coordinates to average distances, ndarray representation)
    """

    if radius < 1 or radius > min(grid.shape):
        raise ValueError(f"Band distance must be greater than 0 and less than min(grid length, grid width)")

    bands = get_bands(grid, radius=radius, absolute_coords=True)
    neighborhoods = get_neighborhoods(
        grid=grid,
        neighbors=Neighbors.COMPLETE,
        exclude_zero=exclude_zero)

    avg_dists = {}
    avg_grid = np.zeros_like(grid).astype(float)

    # iterate over cells in grid (and corresponding bands)
    for band_center, band_cells in bands.items():
        if exclude_zero and grid[band_center[0], band_center[1]] == 0: continue

        # get the central cell's neighborhood
        cell_neighborhood = get_neighborhood(
            grid=grid,
            i=band_center[0],
            j=band_center[1],
            neighbors=Neighbors.COMPLETE,
            exclude_zero=exclude_zero)

        # get each band cell's neighborhood
        band_neighborhoods = {key: neighborhoods[key] for key in band_cells.keys()}

        distances = []
        for n_center, n_cells in band_neighborhoods.items():
            cell_nbrs = []
            band_nbrs = []
            for loc, val in n_cells.items():
                # only compare corresponding neighbors
                if loc not in cell_neighborhood: continue
                cell_nbrs.append(cell_neighborhood[loc[0], loc[1]])
                band_nbrs.append(val)

            if len(cell_nbrs) == 0: continue

            # distance normalized to [0-1]
            radius = hamming_distance(cell_nbrs, band_nbrs) / len(cell_nbrs)
            distances.append(radius)

        if len(distances) == 0: continue

        # compute average distance
        avg_d = float(sum(distances) / len(distances))
        avg_dists[band_center[0], band_center[1]] = avg_d
        avg_grid[band_center[0], band_center[1]] = avg_d

    return avg_dists, avg_grid


def cell_value_distribution(
        grids: List[np.ndarray],
        exclude_zero: bool = False) -> Dict[int, float]:
    """
    Computes the discrete probability distribution of unique cell class values in the given grids.

    :param grids: A list of grids
    :param exclude_zero: Exclude zero-valued cells (interpreted to be missing values)
    :return: The class probability mass
    """

    # flatten the grids into a single list of cells
    cells = flatten(grids)

    # optionally exclude zero-valued cells
    if exclude_zero:
        cells = [cell for cell in cells if cell != 0]

    # count occurrences and compute proportions
    freq = dict(OrderedDict(Counter(cells)))
    uniq = len(freq.keys())
    dist = {k: round(v / sum(freq.values()), uniq) for (k, v) in freq.items()}

    return dist


def undirected_bond_distribution(
        grids: List[np.ndarray],
        exclude_zero: bool = False) -> Tuple[Dict[Tuple[int, int], float], Dict[Tuple[int, int], float]]:
    """
    Computes the discrete probability distribution of undirected transitions (adjacent cell classes) on the given grids.

    :param grids: A list of grids
    :param exclude_zero: Exclude zero-valued cells (interpreted to be missing values)
    :return: A dictionary with key as random variable and value as probablity mass.
    """

    # flatten the grids into a single list of cells
    cells = flatten(grids)

    # optionally exclude zero-valued cells
    if exclude_zero:
        cells = [cell for cell in cells if cell != 0]

    # enumerate undirected pairs
    classes = set(cells)
    sets = set([frozenset([p[0], p[1]]) for p in product(classes, classes)])
    pairs = sorted([(list(p) if len(p) == 2 else list(repeat(next(iter(p)), 2))) for p in sets])

    # dicts to populate
    horiz = {(ca, cb): 0 for ca, cb in pairs}
    vert = horiz.copy()

    for grid in grids:
        w, h = grid.shape

        # count horizontal bonds
        for i, j in product(range(w - 1), range(h)):
            v1 = grid[i, j]
            v2 = grid[i + 1, j]

            # optionally exclude bonds where either cell is zero-valued (missing)
            if exclude_zero and (v1 == 0 or v2 == 0):
                continue

            sk = sorted([int(v1), int(v2)])
            key = (sk[0], sk[1])
            horiz[key] = horiz[key] + 1

        # count vertical bonds
        for i, j in product(range(w), range(h - 1)):
            v1 = grid[i, j]
            v2 = grid[i, j + 1]

            # optionally exclude bonds where either cell is zero-valued (missing)
            if exclude_zero and (v1 == 0 or v2 == 0):
                continue

            sk = sorted([int(v1), int(v2)])
            key = (sk[0], sk[1])
            vert[key] = vert[key] + 1

    # horizontal distribution
    horiz_uniq = len(horiz.keys())
    horiz_sum = sum(horiz.values())
    horiz_dist = {k: round(v / horiz_sum, horiz_uniq) for (k, v) in horiz.items()} if horiz_sum > 0 else horiz

    # vertical distribution
    vert_uniq = len(vert.keys())
    vert_sum = sum(vert.values())
    vert_dist = {k: round(v / vert_sum, vert_uniq) for (k, v) in vert.items()} if vert_sum > 0 else vert

    return horiz_dist, vert_dist


def transition_matrix(
        grid: np.ndarray,
        neighbors: Neighbors = Neighbors.CARDINAL,
        exclude_zero: bool = False) -> np.ndarray:
    """
    Computes the transition matrix for the given grid. The transition matrix is square, with rows
    and columns labeled by classes. Interior cells count transitions between adjacent classes.

    :param grid: The grid
    :param neighbors: The cells to consider neighbors
    :param exclude_zero: Exclude zero-valued cells (interpreted as missing values)
    :return: The transition matrix
    """

    uniq = np.unique(np.ravel(grid))  # get unique classes
    if exclude_zero: uniq = [val for val in uniq if val != 0]  # optionally exclude zeros
    n_uniq = len(uniq)  # number of unique classes
    tmat = np.zeros((n_uniq, n_uniq))  # transition matrix

    # get all neighborhoods and update the transition matrix with each
    nhoods = get_neighborhoods(grid, neighbors=neighbors, exclude_zero=exclude_zero, absolute_coords=True)
    for loc, nbrs in nhoods.items():
        cell = grid[loc[0], loc[1]]
        for cnbr in nbrs.values():
            # subtract 1 to compensate for excluded 0s if needed
            ii = cell - 1 if exclude_zero else cell
            jj = cnbr - 1 if exclude_zero else cnbr
            tmat[ii, jj] += 1

    return tmat
