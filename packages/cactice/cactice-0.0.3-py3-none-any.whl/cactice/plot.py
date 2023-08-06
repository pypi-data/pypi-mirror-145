import math
from typing import Optional, Dict, Tuple, List

import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch, Patch
from matplotlib.ticker import MaxNLocator
import matplotlib.cm as cm
import numpy as np
import seaborn as sns

from cactice.utils import unit_scale


def plot_grid(
        grid: np.ndarray,
        title: Optional[str] = None,
        cmap='Greens',
        patches: List[Patch] = None) -> None:
    # plt.figure(figsize=(20, 20))
    values = list(set(np.ravel(grid)))
    labels = np.vectorize(lambda x: str(x) if x != 0 else '')(grid)
    ax = sns.heatmap(
        grid,
        square=True,
        cbar=False,
        annot=labels,
        fmt='',
        cmap=cmap,
        vmin=0,
        vmax=5 if 0 in values else 4,
        alpha=0.5)
    if title: ax.set_title(title)
    if patches is not None:
        for patch in patches: ax.add_patch(patch)
    plt.show()


def plot_cell_dist(
        dist: Dict[int, float],
        title: str = 'Cell distribution',
        cmap='Greens'):
    ax = sns.barplot(x=[str(k) for k in dist.keys()], y=list(dist.values()), palette=cmap)
    ax.set_title(title)
    # bars = plt.bar(dist.keys(), dist.values())
    # classes = [int(k) for k in dist.keys()]
    # num_classes = len(classes)
    # color = [(c / num_classes * 0.75) for c in classes]
    # for i, b in enumerate(bars): b.set_color(cm.tab20(color[i]))
    # plt.title(title)
    # plt.xlabel("Cell class")
    # plt.ylabel("Proportion")
    # plt.set_cmap(cmap)
    # fig.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.show()


def plot_undirected_bond_dist(
        dist: Dict[Tuple[int, int], float],
        title: str = 'Undirected bond distribution',
        cmap='Greens'):
    # classes = list(set([k[0] for k in dist.keys()]))
    # num_classes = int(math.sqrt(len(dist.keys())))
    # color = [(c / num_classes * 0.75) for c in classes]

    x_axis = np.arange(len(dist.keys()))
    plt.figure(figsize=(20, 6))
    plt.title(title)
    plt.bar(x_axis, dist.values(), 0.8)
    plt.xticks(x_axis, [f"{k[0]}-{k[1]}" for k in dist.keys()])
    plt.xlabel("Bond")
    plt.ylabel("Proportion")
    plt.legend()
    plt.show()


def plot_bond_energies(plot: np.ndarray, energies: Dict[str, float], title: Optional[str] = None) -> None:
    plt.figure(figsize=(14, 14))
    labels = np.vectorize(lambda x: str(int(x)) if x != 0 else '')(plot)
    ax = sns.heatmap(
        plot,
        # center=len(class_freqs.keys()) / 2,
        square=True,
        cbar=False,
        annot=labels,
        fmt='',
        cmap="Greens",
        vmin=0,
        vmax=5,
        alpha=0.5)
    scaled_energies = unit_scale(energies)
    for k, v in scaled_energies.items():
        ks = k.split('_')
        i1 = int(ks[0])
        j1 = int(ks[1])
        i2 = int(ks[2])
        j2 = int(ks[3])
        dx = 1 if j1 == j2 else 0
        dy = 1 if i1 == i2 else 0
        p1 = str(int(plot[j1, i1]))
        p2 = str(int(plot[j2, i2]))

        if not (p1 == '0' or p2 == '0'):
            ax.add_patch(ConnectionPatch(
                (i1 + 0.5, j1 + 0.5),
                (i1 + 0.5 + dx, j1 + 0.5 + dy),
                'data',
                'data',
                shrinkA=1,
                shrinkB=1,
                linewidth=(1 - v) * 30,
                color='blue',
                alpha=(1 - v) * 0.2))

    if title: ax.set_title(title)
    plt.show()
