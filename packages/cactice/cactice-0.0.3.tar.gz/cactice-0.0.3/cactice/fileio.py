import logging
from typing import Dict, List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def read_grid_txt(path: str) -> np.ndarray:
    """
    Reads a grid from the text file at the given path.

    :param path: The text file path
    :return: The pattern as a 2D NumPy array
    """

    with open(path) as file:
        # read all lines in file
        lines = file.readlines()

        # max line length (for padding to rectangularity)
        cols = max([len(line) for line in lines])

        # convert each line (str) to an array of characters
        formatted = []
        for line in lines:
            # strip newlines
            stripped = line.replace('\n', '')

            # pad line
            padded = stripped.ljust(cols - len(stripped), ' ')

            # convert to char array
            formatted.append(list(padded))

        # since we've padded each line to be the same length, numpy interprets a 2D array
        grid = np.array(formatted)

        # we want to work with numeric values, so replace non-numeric features
        seen = dict()
        for (i, j), cell in np.ndenumerate(grid):
            here = grid[i, j]
            if here not in seen.keys(): seen[here] = len(seen.keys())
            grid[i, j] = seen[here]

        return grid.astype(int)


def read_grids_csv(
        path: str,
        name_header: str = 'Grid',
        class_header: str = 'Class',
        row_header: str = 'I',
        col_header: str = 'J') -> Dict[str, np.ndarray]:
    """
    Reads grids from the CSV file at the given path, in the following format:
    <grid name>, <cell class>, <cell row>, <cell column>

    If the first column is not provided, all cells are assumed to lie on the same grid whose name defaults to '1'.

    TODO: If header mappings are provided, the first row is assumed to contain headers and columns are selected according to the given mappings. (If any header mappings are provided, all must be.) If header mappings are not provided, the first row is assumed to contain data and the first 4 columns are assumed name, class, row, and column, in that order.

    :param path: The CSV file path
    :param name_header: The column containing grid names
    :param class_header: the column containing class values (discrete random variable)
    :param row_header: The column containing row indices
    :param col_header: The column containing column indices
    :return: A dictionary containing grids identified by name
    """

    # see if we have headers
    # headers = name_header or class_header or row_header or col_header

    # load the CSV into a data frame
    # TODO: determine whether to read headers or not based on params
    df = pd.read_csv(path, sep=',')

    # if there's only 1 grid and no specified name column, create it
    if name_header not in df: df[name_header] = 1

    grids = dict()
    names = sorted(list(set(df[name_header])))

    for name in names:
        # subset the data frame corresponding to the current grid
        sdf = df.loc[df[name_header] == name]

        # find row and column counts (including missing values)
        rows = max(sdf[row_header]) - min(sdf[row_header]) + 1
        cols = max(sdf[col_header]) - min(sdf[col_header]) + 1

        # initialize grid as empty 2D array
        grid = np.zeros(shape=(rows, cols))

        # loop over cells and populate 2D array
        for i in range(0, rows):
            for j in range(0, cols):

                # check entry at location (i, j)
                matched = sdf.loc[(df[row_header] == i) & (df[col_header] == j)]

                # if missing, fill it in with class = 0 (unknown)
                if len(matched) == 0:
                    cls = 0
                    df = df.append({
                        name_header: name,
                        class_header: cls,
                        row_header: i,
                        col_header: j
                    }, ignore_index=True)
                # otherwise use the given value
                else:
                    cls = matched.to_dict('records')[0][class_header]

                # update the grid
                grid[i, j] = cls

        # save by name and cast values from float (numpy default) to int
        grids[str(name)] = grid.astype(int)

    return grids
