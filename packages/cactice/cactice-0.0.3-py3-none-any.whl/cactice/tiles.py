import logging
from typing import List

import numpy as np

logger = logging.getLogger(__name__)


def find_tile(grid: np.ndarray, target: int, i: int, j: int) -> List[List[int]]:
    """
    Performs a depth-first recursive search for the tile boundaries around the cell at the given location.

    :param grid: The grid
    :param i: The location's row index
    :param j: The location's column index
    :return: A list of cells (specified as [i, j] coordinates) in the tile
    """
    rows = len(grid)
    cols = len(grid[0])

    # get this cell's neighbors in the 4 cardinal directions
    up = grid[i - 1][j] if i > 0 else 0
    down = grid[i + 1][j] if i < rows - 1 else 0
    left = grid[i][j - 1] if j > 0 else 0
    right = grid[i][j + 1] if j < cols - 1 else 0

    # set the current cell to empty to avoid infinite recursion
    grid[i][j] = 0
    tile = [[i, j]]

    # function calls itself on non-empty neighbors
    if up == target: tile = tile + find_tile(grid, target, i - 1, j)
    if down == target: tile = tile + find_tile(grid, target, i + 1, j)
    if left == target: tile = tile + find_tile(grid, target, i, j - 1)
    if right == target: tile = tile + find_tile(grid, target, i, j + 1)

    # otherwise just return what we've got so far
    return tile


def find_tiles(grid: np.ndarray, target: int) -> List[List[List[int]]]:
    """

    :param grid: The grid
    :param target: The target character
    :return: A list of tiles [t0, t1, ... tN], each a list of cells [c0, c1, ..., cN], each a list of coordinates [x, y]
    """

    tiles = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            # if we've chanced upon a target character...
            if grid[i][j] == target:
                # search recursively for the tile it's part of
                tile = find_tile(grid, target, i, j)
                tiles.append(sorted(tile))
                logger.debug(f"Tile {len(tiles)} (size {len(tile)}): {tile}")

    logger.info(f"Found {len(tiles)} tiles")
    return sorted(tiles)
