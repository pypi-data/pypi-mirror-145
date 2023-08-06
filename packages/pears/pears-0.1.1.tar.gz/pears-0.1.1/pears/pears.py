from typing import Any, List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from fastkde import fastKDE


def pears(
    dataset,
    indices: Optional[Any] = None,
    marginal_color: str = "#5E81AC",
    marginal_lw: float = 3.0,
    scatter: bool = True,
    scatter_color: str = "#5E81AC",
    scatter_alpha: float = 0.2,
    scatter_edgecolor: str = "none",
    scatter_thin: int = 1,
    scatter_rasterized: bool = True,
    kde_color: str = "#8FBCBB",
    kde_cmap: str = "bone",
    kde_levels: List[float] = [0.5, 1.0, 1.5, 2.0],
    xlim_quantiles: List[float] = [0.01, 0.99],
    hspace: float = 0.03,
    wspace: float = 0.03,
) -> Tuple[matplotlib.figure.Figure, matplotlib.axes.SubplotBase]:
    """
    Creates a pairs plot with marginal distributions along the diagonals and
    pairwise scatterplots with kernel density estimates in the lower diagonal
    panels.

    Inputs:
    -------
    dataset: obj
        Indexable dataset to plot (e.g., jax/numpy array, dict).

    indices (optional):
        List of indices to access data in `dataset`. Pass this if you only want
        to plot a subset of the data. If None, then uses all indices in `dataset`.

    marginal_color: str = "#5E81AC"
        Color of the marginal KDE line.

    marginal_lw: float = 3.0
        Linewidth of the marginal KDE line.

    scatter: bool = True
        Whether to plot the scatterplots.

    scatter_color: str = "#5E81AC"
        Color of the scatterplot points.

    scatter_alpha: float = 0.2
        Alpha of the scatterplot points.

    scatter_edgecolor: str = "none"
        Edgecolor of the scatterplot points.

    scatter_thin: int = 1
        Thin the dataset by this factor before plotting the scatterplot.
        Use this to speed up plotting.

    scatter_rasterized: bool = True
        Whether to rasterize the scatterplot.

    kde_color: str = "#8FBCBB"
        Color of the KDE contours. Only used if `kde_cmap` is None.

    kde_cmap: str = 'bone'
        Colormap of the KDE contours. Takes precedence over `kde_color` if both
        are passed.

    kde_levels: List[float] = [0.5, 1., 1.5, 2.]
        Sigma levels to plot for the KDE contours.

    xlim_quantiles: List[float] = [0.01, 0.99]
        Quantiles to use for the x-axis limits.

    hspace: float = 0.03
        Gridspec vertical (height) spacing between subplots.

    wspace: float = 0.03
        Gridspec horizontal (width) spacing between subplots.

    Outputs:
    --------

    fig: matplotlib.figure.Figure
        Top level container with all the plot elements.

    ax: matplotlib.axes.SubplotBase
        Axes with matplotlib subplots (2D array of panels).
    """

    assert len(xlim_quantiles) == 2
    assert xlim_quantiles[0] < xlim_quantiles[1]
    assert 0.0 <= xlim_quantiles[0] <= 1.0
    assert 0.0 <= xlim_quantiles[1] <= 1.0

    marginal_kwargs = dict(
        color=marginal_color,
        linewidth=marginal_lw,
    )

    scatter_kwargs = dict(
        color=scatter_color,
        alpha=scatter_alpha,
        edgecolor=scatter_edgecolor,
        rasterized=scatter_rasterized,
    )

    kde_kwargs = dict(
        cmap=kde_cmap,  # cmap has priority
        colors=None if kde_cmap else kde_color,
    )

    # levels outside of kde_kwargs because they need to be scaled later
    levels = 1.0 - np.exp(-0.5 * np.array(kde_levels) ** 2)

    if indices is None:
        if isinstance(dataset, dict):
            indices = list(dataset.keys())
        else:
            indices = np.arange(dataset.shape[0])

    assert indices is not None

    n = len(indices)

    fig, ax = plt.subplots(
        n,
        n,
        figsize=(n * 4 + 2, n * 4),
        gridspec_kw=dict(hspace=hspace, wspace=wspace),  # fmt: skip
    )

    for i in np.arange(n):

        # turn off upper panels
        for j in np.arange(i + 1, n):
            ax[i, j].axis("off")

        # marginal densities in diagonals
        y, x = fastKDE.pdf(dataset[indices[i]])
        ax[i, i].plot(x, y, **marginal_kwargs)
        ax[i, i].set_xlim(*np.quantile(x, np.array(xlim_quantiles)))

        ax[i, i].annotate(
            indices[i], fontsize=35, xy=(0.8, 0.8), xycoords="axes fraction"
        )

        # lower diagonal panels
        for j in np.arange(i):
            # scatter pairs
            if scatter:
                ax[i, j].scatter(
                    dataset[indices[j]][::scatter_thin],
                    dataset[indices[i]][::scatter_thin],
                    **scatter_kwargs
                )

            # kde contours on top
            z, xy = fastKDE.pdf(dataset[indices[j]], dataset[indices[i]])
            x, y = xy
            ax[i, j].contour(x, y, z, levels=z.max() * levels, **kde_kwargs)

        for j in np.arange(n):

            # hacky way to try to make tick positions consistent
            ax[i, j].yaxis.set_major_locator(plt.MaxNLocator(4))
            ax[i, j].xaxis.set_major_locator(plt.MaxNLocator(4))

            # left column:
            #   add label if not diagonal
            #   make the tick labels bigger
            #   rotate tick labels
            if j == 0:
                if i != j:
                    ax[i, j].set_ylabel(indices[i], fontsize=40)
                ax[i, j].tick_params(labelsize=25, labelrotation=45, axis="y")

            # not left column: turn off y tick labels
            else:
                ax[i, j].set_yticklabels([])

            # bottom row:
            #   add labels
            #   make tick labels bigger
            #   rotate tick labels
            if i == n - 1:
                ax[i, j].set_xlabel(indices[j], fontsize=40)
                ax[i, j].tick_params(labelsize=25, labelrotation=45, axis="x")

            # not bottom row: turn off x tick labels
            else:
                ax[i, j].set_xticklabels([])

            # diagonals are special
            if i == j:
                # unless bottom one, remove x labels
                if j != n - 1:
                    ax[i, j].set_xticklabels([])
                    ax[i, j].xaxis.label.set_visible(False)

                # remove y ticks for all
                ax[i, j].set_yticks([])
                ax[i, j].set_yticklabels([])
                ax[i, j].yaxis.label.set_visible(False)

    return fig, ax
