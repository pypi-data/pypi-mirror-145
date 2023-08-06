"""Create reports for validation tool"""
import plotly.figure_factory as ff
import base64
from typing import Union
import xarray as xr
from dataclasses import dataclass
from datetime import datetime
import webbrowser
import os
import numpy as np
from scipy import stats
import pandas as pd
from jinja2 import Environment, PackageLoader
from wind_validation import __version__ as pkg_version
from wind_validation.reporting import plots
import tempfile
from windkit.spatial import reproject
import plotly.graph_objects as go
from plotly.colors import DEFAULT_PLOTLY_COLORS
import warnings
import math

_JINJA_ENV = Environment(loader=PackageLoader("wind_validation", "reporting/templates"))
_SINGLE_POINT_TEMPLATE = "single_point.html"
_AGGREGATED_TEMPLATE = "aggregated.html"
_COMPARISON_TEMPLATE = "comparison.html"
_HTML_STYLE = "style.css"
_SITE_IDENTIFIER = "name"
_POINT_IDENTIFIER = "point"


def create_report(
    validation_results: "Union[list[xr.Dataset], xr.Dataset]",
    **kwargs,
) -> None:
    """Create HTML report from validation results comparing model with data. It is also possible to compare multiple
    model on the same dataset to inspect the performance of different techniques against observations.

    Parameters
    ----------
    validation_results : xarray.Dataset | list[xr.Dataset]
        Validation result produced by main "validate" function. The results are compatible with this reporting function.
        If comparing multiple models a list of datasets can be passed with the same structure as described before.
    obs_name : str | list[str], optional
        Observations site name will be used in the general description of a report. This can be string when comparing
        single model to single observation dataset however when making comparison the list of names is required because
        otherwise there is no way to make a distinction between models.
    mod_name : str | list[str], optional
        Model name will be used in the general description of a report. This can be string when comparing
        single model to single observation dataset however when making comparison the list of names is required because
        otherwise there is no way to make a distinction between models.
    dest : str, optional
        Path of the html file to write the report to. If not provided html file is saved in tmp directory.
        By default None
    author : str, optional
        Author of the generated report to be stated in the description.
        By default ""
    show : bool, optional
        If True - tries to open the report in the browser right away.
        By default False

    Raises
    ------
    RuntimeError
        If destination folder doesn't exist the generation will fail.
        If results type doesn't match the documented ones.
        If model and observation names are not provided for comparison report.
    """

    html = None
    if type(validation_results) == xr.Dataset:
        # Old logic for distinguishing agg from single point/site, leaving it for
        # future reference if the discussion comes up again :)
        # if (
        #     _SITE_IDENTIFIER not in validation_results.dims
        #     or validation_results.dims[_SITE_IDENTIFIER] == 1
        # ):
        if (
            _POINT_IDENTIFIER in validation_results.dims
            and validation_results.dims[_POINT_IDENTIFIER] > 1
        ):
            # for plotting purpose we always want the dataset to be in lat/long
            validation_results = reproject(validation_results, "EPSG:4326")
            # single site (multiple points) or points from various sites vs a model
            html = __aggregated_report(validation_results, **kwargs)
        else:
            # single point vs a model
            html = __single_point_report(validation_results, **kwargs)

    elif type(validation_results) == list:
        for i in range(len(validation_results)):
            if type(validation_results[i]) != xr.Dataset:
                raise RuntimeError(
                    "Validation result must be xarray.Dataset type."
                    "One of the provided results does not meet the criterion"
                )
            validation_results[i] = reproject(validation_results[i], "EPSG:4326")
        # useful for multiple models comparison on same sites data
        html = __comparison_report(validation_results, **kwargs)

    else:
        raise RuntimeError(
            "Can't create a report from this type of data!"
            "Available options: list[xr.Dataset], xr.Dataset"
        )

    dest = kwargs.get("dest", None)
    if dest is None:
        reportf = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        dest = reportf.name
    else:
        try:
            reportf = open(dest, "wb")
        except:  # pragma: no cover
            raise RuntimeError("Provided directory doesn't exist...")
    reportf.write(html.encode("utf-8"))
    print(f"HTML report saved in: {dest}")
    show = kwargs.get("show", True)
    if not show:  # pragma: no cover
        return
    success = webbrowser.open(dest, new=2)
    if not success:
        print("Couldn't open a browser window!")


@dataclass
class MetaData:
    """Package and report metadata"""

    date: datetime
    user: str
    version: str


@dataclass
class ValidationResults:
    """Validation results class includes the observation title,
    model title and results from validation comparing those two"""

    obs: str
    mod: str
    site_results: pd.DataFrame
    format: str


def __preprocess_args(validation_results: xr.Dataset, **kwargs):
    if "format" not in validation_results.attrs:
        raise RuntimeError("Validation results are missing format attribute")
    if len(validation_results.dims) == 0:
        validation_results = validation_results.expand_dims("point")
    res_format = validation_results.attrs["format"]
    author = kwargs.get("author", "")
    site_name = kwargs.get("obs_name", "Observations")
    model_name = kwargs.get("mod_name", "Model")
    # if meaningfull names are available, use these, otherwise use
    # the enumerated point dimension (default)
    try:
        validation_results = (
            validation_results.to_dataframe()
            .reset_index()
            .set_index([_SITE_IDENTIFIER])
        )
    except:
        validation_results = validation_results.to_dataframe()
    meta = MetaData(datetime.now(), author, pkg_version)
    results = ValidationResults(site_name, model_name, validation_results, res_format)
    return (meta, results)


def __aggregate(results: ValidationResults):
    try:
        agg_vars = results.site_results[
            [
                "obs_wind_speed_mean",
                "mod_wind_speed_mean",
                "wind_speed_me",
                "wind_speed_mpe",
                "wind_speed_mae",
                "wind_speed_mape",
                "obs_power_density_mean",
                "mod_power_density_mean",
                "power_density_me",
                "power_density_mpe",
                "power_density_mae",
                "power_density_mape",
            ]
        ]
    except KeyError as e:
        raise RuntimeError(
            f"Validation result is missing some"
            f" assumed keys to create a report:\n{e}"
        )
    agg_res = agg_vars.aggregate(np.mean)
    return agg_res


def __aggregated_report(
    validation_results: xr.Dataset,
    **kwargs,
):
    meta, results = __preprocess_args(validation_results, **kwargs)
    agg_results = __aggregate(results)

    css_content = f"<style>{_JINJA_ENV.get_template(_HTML_STYLE).render()}</style>"

    mapes = plots._individual_mast_maep(
        plots.PlotResult(
            results.site_results["wind_speed_mpe"], "Wind speed error", "%"
        )
    )
    for i, fig in enumerate(mapes):
        mapes[i] = plots._fig_to_html(fig)

    # TODO should raise error for singple point
    power_hist = plots._compare_distributions(
        plots.PlotResult(results.site_results, "Power density error", "%"),
        ["power_density_mpe"],
        [f"{results.obs} vs {results.mod}"],
    )

    ws_hist = plots._compare_distributions(
        plots.PlotResult(results.site_results, "Wind speed error", "%"),
        ["wind_speed_mpe"],
        [f"{results.obs} vs {results.mod}"],
    )

    template_html = _JINJA_ENV.get_template(_AGGREGATED_TEMPLATE)
    rendered_html = template_html.render(
        title=f"Wind-Validation Aggregated {results.format.title()} Report",
        md_css=css_content,
        obs=results.obs,
        mod=results.mod,
        meta=meta,
        agg_results=agg_results,
        site_results=results.site_results,
        mae_hist=plots._fig_to_html(ws_hist),
        power_mape_hist=plots._fig_to_html(power_hist),
        mapes=mapes,
        iterrow=list(results.site_results.iterrows()),
        logos=__generate_bin_logos(),
    )

    return rendered_html


def __comparison_report(validation_results: "list[xr.Dataset]", **kwargs):
    # parse names
    if "obs_name" not in kwargs or "mod_name" not in kwargs:
        raise RuntimeError(
            "Comparison report requires list of model and observation names!"
        )
    if type(kwargs["obs_name"]) != list and type(kwargs["mod_name"]) != list:
        raise RuntimeError(
            "Comparison report requires list of model and observation names!"
        )
    models = kwargs["mod_name"]
    if all([m == models[0] for m in models[1:]]):
        warnings.warn(
            "All the model names are the same, you are either passing "
            "observation names instead of models or want to compare "
            "different observations with the same model which"
            "doesn't make sense because (in some plots) the comparison "
            "is done side by side on each point."
        )
    observations = kwargs["obs_name"]

    points_num = validation_results[0].dims["point"]
    if not all([x.dims["point"] == points_num for x in validation_results]):
        raise RuntimeError("Cannot compare non-equally sized validation results.")

    # TODO: fix all the ugly plotting stuff, isolate it
    nbins = 30
    slice_by = 35  # split individual points comparison into multiple figs
    aggregated_results = []
    tabledf = pd.DataFrame()
    mapdf = pd.DataFrame()
    hist_plots = {"wind_speed": go.Figure(), "power_density": go.Figure()}
    for i, val_res in enumerate(validation_results):
        meta, results = __preprocess_args(
            val_res, **kwargs  # val_res.drop_vars(_SITE_IDENTIFIER, errors="ignore")
        )
        agg_res = __aggregate(results)
        aggregated_results.append(agg_res)
        number_of_sites = len(results.site_results.index.unique())
        number_of_points = len(results.site_results.index)
        n_fig = math.ceil(number_of_sites / slice_by)
        if i == 0:
            wind_speed_mpe_bars = [go.Figure() for x in range(n_fig)]
        # loop over two variables that we want to plot
        for v in hist_plots.keys():
            data = results.site_results[f"{v}_mpe"]
            mean = data.mean()
            stddev = data.std()
            xrange = np.linspace(data.min(), data.max(), nbins)
            hist_plots[v].add_trace(
                go.Histogram(
                    x=results.site_results[f"{v}_mpe"],
                    nbinsx=nbins,
                    histnorm="probability density",
                    marker=dict(color=DEFAULT_PLOTLY_COLORS[i]),
                    name=models[i] + " vs " + observations[i],
                )
            )
            hist_plots[v].add_trace(
                go.Scatter(
                    x=xrange,
                    y=stats.norm(loc=mean, scale=stddev).pdf(xrange),
                    mode="lines",
                    line=dict(color=DEFAULT_PLOTLY_COLORS[i], width=1.5),
                    name=f"Normal dist. ({models[i]})",
                )
            )

        for k in range(n_fig):
            lower = k * slice_by
            upper = lower + slice_by
            if number_of_sites / number_of_points == 1:
                sliced = results.site_results[lower:upper]
                wind_speed_mpe_bars[k].add_trace(
                    go.Bar(
                        name=models[i] + " vs " + observations[i],
                        x=sliced.index.values,
                        y=sliced.wind_speed_mpe,
                    )
                )
            else:
                sliced = results.site_results.loc[
                    results.site_results.index.unique()[lower:upper]
                ]
                wind_speed_mpe_bars[k].add_trace(
                    go.Box(
                        name=models[i] + " vs " + observations[i],
                        x=sliced.index.values,
                        y=sliced.wind_speed_mpe,
                    )
                )

        # required because the following code requires merging by unique point
        # the above code indexing by name to be able to plot boxplots
        meta, results = __preprocess_args(
            val_res.drop_vars(_SITE_IDENTIFIER, errors="ignore"), **kwargs  # val_res
        )
        suffixed_df = results.site_results[  # form detailed table
            ["wind_speed_mpe", "power_density_mpe"]
        ]
        suffixed_df = suffixed_df.add_suffix(f"_model_{models[i]}")
        tabledf = pd.concat(
            [tabledf, suffixed_df],
            axis=1,
        )

        results.site_results["model"] = models[i]
        mapdf = pd.concat([mapdf, results.site_results])

    # pretty column names for table
    tabledf.rename(
        columns=lambda x: " ".join(
            [y.capitalize() if y != "ME" else y.upper() for y in x.split("_")]
        ),
        inplace=True,
    )
    tabledf = tabledf.reindex(sorted(tabledf.columns), axis=1)
    tabledf.index.names = ["Point/Site"]
    tabledf.reset_index(inplace=True)
    tabledf = tabledf.round(1)
    pd_html_table = tabledf.to_html(
        index=False, classes=["sortable", "center"], border=0
    )
    table_caption = f"""<caption>
        Table 2: detailed all-sector metrics for each of the {number_of_points} points.
    </caption>"""
    pd_html_table = pd_html_table.replace("<thead>", table_caption + "<thead>")

    for i in range(n_fig):
        wind_speed_mpe_bars[i].update_layout(  # TODO: dynamic name?
            xaxis_title="Points", yaxis_title="Wind Speed MPE"
        )
        wind_speed_mpe_bars[i].update_layout(barmode="group", legend=dict(x=0, y=1))
        wind_speed_mpe_bars[i] = plots._fig_to_html(wind_speed_mpe_bars[i])

    hist_plots["wind_speed"].update_layout(
        xaxis_title="Mean error in wind speed (%)",
        yaxis_title="Probability density",
        legend=dict(x=0, y=1),
    )
    hist_plots["power_density"].update_layout(
        xaxis_title="Mean error in power density (%)",
        yaxis_title="Probability density",
        legend=dict(x=0, y=1),
    )

    template_html = _JINJA_ENV.get_template(_COMPARISON_TEMPLATE)
    rendered_html = template_html.render(
        title=f"Wind-Validation Comparison {results.format.title()} Report",
        md_css=f"<style>{_JINJA_ENV.get_template(_HTML_STYLE).render()}</style>",
        obs=observations,
        mod=models,
        point_count=number_of_points,
        mast_count=number_of_sites,
        # zip is limited by iterating only once, thus is wrapper in list
        mod_obs_agg=list(zip(models, observations, aggregated_results)),
        meta=meta,
        wind_speed_mpe_hist=plots._fig_to_html(hist_plots["wind_speed"]),
        power_density_mae_hist=plots._fig_to_html(hist_plots["power_density"]),
        wind_speed_mpe_bars=wind_speed_mpe_bars,
        pandas_table=pd_html_table,
        map_points=list(mapdf.iterrows()),
        logos=__generate_bin_logos(),
    )

    return rendered_html


def __single_point_report(validation_results: xr.Dataset, **kwargs):
    meta, results = __preprocess_args(validation_results, **kwargs)
    css_content = f"<style>{_JINJA_ENV.get_template(_HTML_STYLE).render()}</style>"
    template_html = _JINJA_ENV.get_template(_SINGLE_POINT_TEMPLATE)

    newdf = pd.DataFrame()
    newdf.index.names = ["Variable"]
    newdf.assign(Variable=results.site_results.columns)
    newdf = newdf.assign(Value=results.site_results.iloc[0])
    newdf.reset_index(inplace=True)
    newdf = newdf.to_html(index=False, classes=["center"], border=0)
    table_caption = f"""<caption>
        Table 1: Detailed site/point metrics & stats. Wind-validation (2021).
    </caption>"""
    newdf = newdf.replace("<thead>", table_caption + "<thead>")

    return template_html.render(
        title=f"Wind-Validation Aggregated {results.format.title()} Report",
        md_css=css_content,
        obs=results.obs,
        mod=results.mod,
        meta=meta,
        iterrow=list(results.site_results.iterrows()),
        logos=__generate_bin_logos(),
        table=newdf,
    )


def __generate_bin_logos():
    def _encode_img(path):
        encoded_string = ""
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode()
        return encoded_string

    dtu_logo = _encode_img(
        os.path.dirname(os.path.realpath(__file__))
        + "/templates/static/Corp_Red_RGB.png"
    )

    winsider_logo = _encode_img(
        os.path.dirname(os.path.realpath(__file__))
        + "/templates/static/Windsider_BIG_Logo_Color.png"
    )

    return (dtu_logo, winsider_logo)
