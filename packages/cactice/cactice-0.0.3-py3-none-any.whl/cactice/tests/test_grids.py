from matplotlib.patches import Rectangle

from cactice.fileio import read_grids_csv
from cactice.grids import get_band, get_neighborhood, Neighbors
from cactice.plot import plot_grid


def test_get_neighbors_cardinal_interior():
    grid = grids['4']
    cell = (5, 8)
    neighbors = get_neighborhood(grid, cell[0], cell[1], Neighbors.CARDINAL, absolute_coords=True)

    # debugging
    # patches = [Rectangle((loc[0], loc[1]), 1, 1, fill=False, edgecolor='blue', lw=3) for loc in neighbors.keys()]
    # patches.append(Rectangle((cell[0], cell[1]), 1, 1, fill=False, edgecolor='green', lw=3))
    # plot_grid(grid, patches=patches)

    assert len(neighbors) == 4


def test_get_neighbors_diagonal_interior():
    grid = grids['4']
    cell = (5, 8)
    neighbors = get_neighborhood(grid, cell[0], cell[1], Neighbors.DIAGONAL, absolute_coords=True)

    # debugging
    # patches = [Rectangle((loc[0], loc[1]), 1, 1, fill=False, edgecolor='blue', lw=3) for loc in neighbors.keys()]
    # patches.append(Rectangle((cell[0], cell[1]), 1, 1, fill=False, edgecolor='green', lw=3))
    # plot_grid(grid, patches=patches)

    assert len(neighbors) == 4


def test_get_neighbors_complete_interior():
    grid = grids['4']
    cell = (5, 8)
    neighbors = get_neighborhood(grid, cell[0], cell[1], Neighbors.COMPLETE, absolute_coords=True)

    # debugging
    # patches = [Rectangle((loc[0], loc[1]), 1, 1, fill=False, edgecolor='blue', lw=3) for loc in neighbors.keys()]
    # patches.append(Rectangle((cell[0], cell[1]), 1, 1, fill=False, edgecolor='green', lw=3))
    # plot_grid(grid, patches=patches)

    assert len(neighbors) == 8


def test_get_neighbors_cardinal_boundary():
    grid = grids['4']
    cell = (0, 1)
    neighbors = get_neighborhood(grid, cell[0], cell[1], Neighbors.CARDINAL, absolute_coords=True)

    # debugging
    # patches = [Rectangle((loc[0], loc[1]), 1, 1, fill=False, edgecolor='blue', lw=3) for loc in neighbors.keys()]
    # patches.append(Rectangle((cell[0], cell[1]), 1, 1, fill=False, edgecolor='green', lw=3))
    # plot_grid(grid, patches=patches)

    assert len(neighbors) == 3
    assert (0, 0) in neighbors.keys()
    assert (0, 2) in neighbors.keys()
    assert (1, 1) in neighbors.keys()


def test_get_neighbors_diagonal_boundary():
    grid = grids['4']
    cell = (0, 1)
    neighbors = get_neighborhood(grid, cell[0], cell[1], Neighbors.DIAGONAL, absolute_coords=True)

    # debugging
    # patches = [Rectangle((loc[0], loc[1]), 1, 1, fill=False, edgecolor='blue', lw=3) for loc in neighbors.keys()]
    # patches.append(Rectangle((cell[0], cell[1]), 1, 1, fill=False, edgecolor='green', lw=3))
    # plot_grid(grid, patches=patches)

    assert len(neighbors) == 2
    assert (1, 0) in neighbors.keys()
    assert (1, 2) in neighbors.keys()


def test_get_neighbors_complete_boundary():
    grid = grids['4']
    cell = (0, 1)
    neighbors = get_neighborhood(grid, cell[0], cell[1], Neighbors.COMPLETE, absolute_coords=True)

    # debugging
    # patches = [Rectangle((loc[0], loc[1]), 1, 1, fill=False, edgecolor='blue', lw=3) for loc in neighbors.keys()]
    # patches.append(Rectangle((cell[0], cell[1]), 1, 1, fill=False, edgecolor='green', lw=3))
    # plot_grid(grid, patches=patches)

    assert len(neighbors) == 5
    assert (0, 0) in neighbors.keys()
    assert (0, 2) in neighbors.keys()
    assert (1, 1) in neighbors.keys()
    assert (1, 0) in neighbors.keys()
    assert (1, 2) in neighbors.keys()


grids = read_grids_csv('testdata/grids.csv')


def test_get_band():
    grid = grids['4']
    cell = (5, 8)

    # TODO: if we allow start=0, reinstate this
    # trivial case
    # start = 0
    # band = get_band(grid, i=cell[0], j=cell[1], start=start)
    # assert len(band.keys()) == 1
    # assert band[(start, start)] == grid[(cell[0], cell[1])]
    # band = get_band(grid, i=cell[0], j=cell[1], start=start, absolute_coords=True)
    # assert len(band.keys()) == 1
    # assert band[(cell[0], cell[1])] == grid[(cell[0], cell[1])]

    # immediate 8-cell (cardinal & diagonal) neighborhood
    start = 1
    band = get_band(grid, i=cell[0], j=cell[1], radius=start)
    assert len(band.keys()) == 8
    assert band[(start, start)] == grid[(cell[0] + start, cell[1] + start)]
    assert band[(-1 * start, -1 * start)] == grid[(cell[0] - start, cell[1] - start)]
    band = get_band(grid, i=cell[0], j=cell[1], radius=start, absolute_coords=True)
    assert len(band.keys()) == 8
    assert band[(cell[0] + start, cell[1] + start)] == grid[(cell[0] + start, cell[1] + start)]
    assert band[(cell[0] - start, cell[1] - start)] == grid[(cell[0] - start, cell[1] - start)]

    # the next layer out
    start = 2
    band = get_band(grid, i=cell[0], j=cell[1], radius=start)
    assert len(band.keys()) == 16
    assert band[(start, start)] == grid[(cell[0] + start, cell[1] + start)]
    assert band[(-1 * start, -1 * start)] == grid[(cell[0] - start, cell[1] - start)]
    band = get_band(grid, i=cell[0], j=cell[1], radius=start, absolute_coords=True)
    assert len(band.keys()) == 16
    assert band[(cell[0] + start, cell[1] + start)] == grid[(cell[0] + start, cell[1] + start)]
    assert band[(cell[0] - start, cell[1] - start)] == grid[(cell[0] - start, cell[1] - start)]
