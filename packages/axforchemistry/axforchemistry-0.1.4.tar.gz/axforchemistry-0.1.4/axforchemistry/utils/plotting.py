from os import path
from pathlib import Path
from ax.modelbridge.cross_validation import cross_validate
from ax.plot.diagnostic import interact_cross_validation_plotly, tile_cross_validation
from plotly import offline
import plotly.graph_objects as go


def matplotlibify(fig, size=24, width_inches=3.5, height_inches=3.5, dpi=142):
    # make it look more like matplotlib
    # modified from: https://medium.com/swlh/formatting-a-plotly-figure-with-matplotlib-style-fa56ddd97539)
    font_dict = dict(family="Arial", size=size, color="black")

    fig.update_layout(
        font=font_dict,
        plot_bgcolor="white",
        width=width_inches * dpi,
        height=height_inches * dpi,
        margin=dict(r=40, t=20, b=10),
    )

    fig.update_yaxes(
        showline=True,  # add line at x=0
        linecolor="black",  # line color
        linewidth=2.4,  # line size
        ticks="inside",  # ticks outside axis
        tickfont=font_dict,  # tick label font
        mirror="allticks",  # add ticks to top/right axes
        tickwidth=2.4,  # tick width
        tickcolor="black",  # tick color
    )

    fig.update_xaxes(
        showline=True,
        showticklabels=True,
        linecolor="black",
        linewidth=2.4,
        ticks="inside",
        tickfont=font_dict,
        mirror="allticks",
        tickwidth=2.4,
        tickcolor="black",
    )
    fig.update(layout_coloraxis_showscale=False)

    width_default_px = fig.layout.width
    targ_dpi = 300
    scale = width_inches / (width_default_px / dpi) * (targ_dpi / dpi)

    return fig, scale


def to_plotly(axplotconfig):
    data = axplotconfig[0]["data"]
    layout = axplotconfig[0]["layout"]
    fig = go.Figure({"data": data, "layout": layout})
    return fig


def cv_plot(model, figdir=None, fname=None, matplotlibify_kwargs={}):
    cv_results = cross_validate(model)
    fig = interact_cross_validation_plotly(cv_results)
    offline.plot(fig)

    tile_fig = to_plotly(tile_cross_validation(cv_results))
    # remove the titles, consider saving individually per metric
    # or add (a), (b), (c), etc.
    # add parity lines
    offline.plot(tile_fig)

    if figdir is not None and fname is not None:
        if figdir is None or fname is None:
            raise ValueError("specify figdir and figname or neither")
        Path(figdir).mkdir(exist_ok=True, parents=True)
        figpath = path.join(figdir, fname)
        fig.write_html(figpath + ".html")
        fig.to_json(figpath + ".json")

        tile_fig, _ = matplotlibify(tile_fig, **matplotlibify_kwargs)
        tile_fig.write_image(figpath + ".png")

    return cv_results, fig, tile_fig

