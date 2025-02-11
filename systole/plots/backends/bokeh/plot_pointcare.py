# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

from typing import List, Optional, Tuple, Union

import numpy as np
from bokeh.models import Arrow, NormalHead
from bokeh.plotting import figure
from bokeh.plotting.figure import Figure

from systole.hrv import nonlinear


def plot_pointcare(
    rr: np.ndarray,
    figsize: Optional[Union[List[int], Tuple[int, int], int]] = None,
    ax=None,
) -> Figure:
    """Pointcare plot.

    Parameters
    ----------
    rr : np.ndarray
        RR intervals (miliseconds).
    figsize : list, tuple, int or None
        Figure size. Default is `(13, 5)`.
    ax : :class:`matplotlib.axes.Axes` or None
        Where to draw the plot. Default is `None` (create a new figure).

    Returns
    -------
    pointcare_plot : :class:`bokeh.plotting.figure.Figure`
        The pointcare plot.

    """
    if figsize is None:
        height, width = 400, 400
    elif isinstance(figsize, int):
        height, width = figsize, figsize
    else:
        width, height = figsize

    if np.any(rr >= 3000) | np.any(rr <= 200):

        # Set outliers to reasonable values for plotting
        rr[np.where(rr > 3000)[0]] = 3000
        rr[np.where(rr < 200)[0]] = 200

    # Create x and y vectors
    rr_x, rr_y = rr[:-1], rr[1:]

    # Find outliers idx
    outliers = (rr_x == 3000) | (rr_x == 200) | (rr_y == 3000) | (rr_y == 200)
    range_min, range_max = rr.min() - 50, rr.max() + 50

    pointcare_plot = figure(
        title="Pointcaré plot",
        plot_height=height,
        plot_width=width,
        x_axis_label="RR (n)",
        y_axis_label="RR (n+1)",
        output_backend="webgl",
        x_range=[range_min, range_max],
        y_range=[range_min, range_max],
    )

    # Identity line
    pointcare_plot.line(
        [range_min, range_max], [range_min, range_max], color="grey", line_dash="dashed"
    )

    # Compute SD1 and SD2 metrics
    df = nonlinear(rr)
    sd1 = df[df["Metric"] == "SD1"]["Values"].values[0]
    sd2 = df[df["Metric"] == "SD2"]["Values"].values[0]

    # Ellipse
    pointcare_plot.ellipse(
        x=rr_x[~outliers].mean(),
        y=rr_y[~outliers].mean(),
        height=sd1 * 2,
        width=sd2 * 2,
        angle=np.pi / 4,
        fill_alpha=0.4,
        fill_color="#a9373b",
        line_alpha=1.0,
        line_width=3,
        line_color="gray",
        line_dash="dashed",
    )

    # Scatter plot - valid intervals only
    pointcare_plot.circle(
        rr_x[~outliers],
        rr_y[~outliers],
        size=2.5,
        fill_color="#4c72b0",
        line_color="gray",
        alpha=0.2,
    )

    # Scatter plot - outliers
    pointcare_plot.circle(
        rr_x[outliers], rr_y[outliers], size=5, color="#a9373b", alpha=0.8
    )

    # SD1 arrow
    pointcare_plot.add_layout(
        Arrow(
            end=NormalHead(fill_color="blue", size=10),
            x_start=rr_x[~outliers].mean(),
            y_start=rr_y[~outliers].mean(),
            x_end=rr_x[~outliers].mean() + (-sd1 * np.cos(np.deg2rad(45))),
            y_end=rr_y[~outliers].mean() + sd1 * np.sin(np.deg2rad(45)),
        )
    )

    # SD2 arrow
    pointcare_plot.add_layout(
        Arrow(
            end=NormalHead(fill_color="green", size=10),
            x_start=rr_x[~outliers].mean(),
            y_start=rr_y[~outliers].mean(),
            x_end=rr_x[~outliers].mean() + sd2 * np.cos(np.deg2rad(45)),
            y_end=rr_y[~outliers].mean() + sd2 * np.sin(np.deg2rad(45)),
        )
    )

    return pointcare_plot
