"""Plots for wind validation"""
import math
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Union

import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


@dataclass
class PlotResult:
    """Required to get metadata for plot"""

    data: Union[pd.Series, pd.DataFrame]
    var_name: str
    var_units: str


def _unit_label(data: PlotResult):
    return f"{data.var_name} ({data.var_units})"


def _fig_to_html(fig, online=True):
    if online:
        return fig.to_html(include_plotlyjs="cdn", full_html=False)
    else:
        return fig.to_html(full_html=False)


def _individual_mast_maep(data: PlotResult, slice_by=35):
    figs = []
    number_of_sites = len(data.data.index.unique())
    number_of_points = len(data.data.index)
    n_fig = math.ceil(number_of_sites / slice_by)
    for i in range(n_fig):
        lower = i * slice_by
        upper = lower + slice_by
        if number_of_sites / number_of_points == 1:
            sliced = data.data[lower:upper]
            fig = go.Figure(
                data=[go.Bar(x=sliced.index, y=sliced)],
            )
        else:
            sliced = data.data.loc[data.data.index.unique()[lower:upper]]
            fig = go.Figure(
                data=[go.Box(x=sliced.index, y=sliced)],
            )
        fig.update_layout(
            xaxis_title="Mast",
            yaxis_title=_unit_label(data),
        )
        figs.append(fig)

    return figs


def _error_distribution(data: PlotResult, binsize: int):
    """Create a histogram of an error metric

    Parameters
    ----------
    data : PlotResult
        Data to be plotted
    binsize : float
        Size of the bins in the units of the data

    Returns
    -------
    plotly.graph_objs._figure.Figure
        Plotly histogram
    """

    nbins = int((data.data.max() - data.data.min()) / binsize)
    return px.histogram(x=data.data, labels={"x": _unit_label(data)}, nbins=nbins)


def _compare_distributions(data, columns, labels, nrbins=30):
    all_plots = []
    for c, l in zip(columns, labels):
        mean = data.data[c].mean()
        stddev = data.data[c].std()
        xrange = np.linspace(data.data[c].min(), data.data[c].max(), nrbins)
        all_plots.append(
            go.Histogram(
                x=data.data[c], nbinsx=nrbins, histnorm="probability density", name=l
            )
        )
        all_plots.append(
            go.Scatter(
                x=xrange,
                y=stats.norm(loc=mean, scale=stddev).pdf(xrange),
                mode="lines",
                line=dict(width=1.5),
                name=f"Normal dist. ({l})",
            )
        )
    fig = go.Figure(data=all_plots)
    fig.update_layout(
        xaxis={"title": {"text": _unit_label(data)}},
        yaxis={"title": {"text": "Probability density"}},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
