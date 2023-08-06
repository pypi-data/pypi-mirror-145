import logging
import random
from typing import List, Dict

import numpy as np

import cactice.grids
from cactice.grids import Neighbors, get_neighborhood


class RNS:
    def __init__(
            self,
            neighbors: Neighbors = Neighbors.CARDINAL):
        """
        Create a random neighbor selection model.
        This model assigns to each cell by simply selecting at random from its neighbors.
        If no neighbors are known, a value is randomly selected from the observed class distribution.

        :param neighbors: The cells to consider part of the neighborhood.
        """

        self.__logger = logging.getLogger(__name__)
        self.__fit: bool = False
        self.__neighbors: Neighbors = neighbors
        self.__train: List[np.ndarray] = []
        self.__cell_distribution: Dict[str, float] = {}

    def fit(self, grids: List[np.ndarray] = None):
        """
        Fit the model to the given grids.
        """

        self.__train = grids
        self.__cell_distribution = cactice.grids.cell_value_distribution(grids, exclude_zero=True)
        self.__fit = True

    def predict(self, grids: List[np.ndarray] = None) -> List[np.ndarray]:
        """
        Predict missing cells on the training grids or on the given grids (if provided).
        To generate entirely novel grids conditioned on the training set, provide a list of empty (zero-valued) arrays.

        :param grids: The grids to predict on (the training set will be used otherwise)
        :return: The grids with missing values filled in.
        """

        if not self.__fit:
            raise ValueError(f"Model must be fit before predictions can be made!")

        # initialize grids to predict on
        grid_predictions = [np.copy(grid) for grid in (grids if grids is not None else self.__train)]

        for gi, grid in enumerate(grid_predictions):
            # find cells to predict (missing locations)
            rows = range(0, grid.shape[0])
            cols = range(0, grid.shape[1])
            grid_pred = grid_predictions[gi].copy()
            missing = [(i, j) for i in rows for j in cols if grid_pred[i, j] == 0]

            # if this grid has no missing locations, skip it
            if len(missing) == 0: continue

            # predict cells one by one
            for (i, j) in missing:
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

                # predict cell value by making a random selection from its neighbors, if any
                # or if none, choosing randomly according to the observed class distribution
                if len(neighbors) > 0:
                    self.__logger.debug(f"Assigning location ({i}, {j}) via RNS")
                    cell_pred = random.choice(neighbors)
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
