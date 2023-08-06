# (c) 2022 DTU Wind Energy
"""
Vertical profile plotting
"""


from ._helpers import (
    missing_arguments,
    check_plotting_attrs,
    HAS_PLOTLY,
    requires_plotly,
)

if HAS_PLOTLY:
    import plotly.express as px


def vertical_profile(
    da_meas=None, da_pred=None, color_bwc="red", color_wwc="dodgerblue"
):
    """Plots the vertical profile of the dataArray or dataArrays introduced. If
    two dataArrays are given, one should represent mesured/observed data (as the one
    represented in a binned wind climate) and the other predicted/generalized
    data (as the one represented in a weibull wind climate). The function will
    plot both vertical profiles to compare.
    If one dataArray is give, the function plots its vertical profile.

    Parameters
    ----------
    da_meas : xarray.DataArray
        WindKit DataArray representing a mesured/observed vertical profile data.

    da_pred : xarray.DataArray
        WindKit DataArray representing a predicted/generalized vertical profile data.

    color_bwc :  str, optional
        Sets the color of the mesured/observed vertical profile plot.
        Strings should define valid CSS-colors.
        By default is defined as "red".

    color_wwc :  str, optional
        Sets the color of the predicted/generalized vertical profile plot.
        Strings should define valid CSS-colors.
        By default is defined as "dodgerblue".

    Returns
    -------
    plotly.graph_objects.Figure
        Plotly figure for display, additional modification, or output

    """
    requires_plotly()

    if da_meas is not None and da_pred is not None:
        da_meas = da_meas.squeeze()
        df_bwc = da_meas.to_dataframe().reset_index().dropna()
        da_pred = da_pred.squeeze()
        df_wwc = da_pred.to_dataframe().reset_index().dropna()

        plot_bwc_dict = {
            "x": da_meas.name,
            "y": "height",
            "custom_data": [da_meas.name, "height"],
            "color_discrete_sequence": [color_bwc],
        }
        plot_wwc_dict = {
            "x": da_pred.name,
            "y": "height",
            "custom_data": [da_pred.name, "height"],
            "color_discrete_sequence": [color_wwc],
        }

        for da in [da_meas, da_pred]:
            xaxes_title = check_plotting_attrs(da)
            yaxes_title = check_plotting_attrs(da["height"])

        fig = px.scatter(df_bwc, **plot_bwc_dict)
        fig["data"][0]["name"] = "Mesured"
        fig["data"][0]["showlegend"] = True

        fig2 = px.line(df_wwc, **plot_wwc_dict)
        fig2["data"][0]["name"] = "Predicted"
        fig2["data"][0]["showlegend"] = True
        fig.add_trace(fig2.data[0])

    elif da_meas is not None and da_pred is None:
        da_meas = da_meas.squeeze()
        df_bwc = da_meas.to_dataframe().reset_index().dropna()

        plot_bwc_dict = {
            "x": da_meas.name,
            "y": "height",
            "custom_data": [da_meas.name, "height"],
            "color_discrete_sequence": [color_bwc],
        }

        xaxes_title = check_plotting_attrs(da_meas)
        yaxes_title = check_plotting_attrs(da_meas["height"])

        fig = px.scatter(df_bwc, **plot_bwc_dict)
        fig["data"][0]["name"] = "Mesured"
        fig["data"][0]["showlegend"] = True

    elif da_meas is None and da_pred is not None:
        da_pred = da_pred.squeeze()
        df_wwc = da_pred.to_dataframe().reset_index().dropna()

        plot_wwc_dict = {
            "x": da_pred.name,
            "y": "height",
            "custom_data": [da_pred.name, "height"],
            "color_discrete_sequence": [color_wwc],
        }

        xaxes_title = check_plotting_attrs(da_pred)
        yaxes_title = check_plotting_attrs(da_pred["height"])

        fig = px.line(df_wwc, **plot_wwc_dict)
        fig["data"][0]["name"] = "Predicted"
        fig["data"][0]["showlegend"] = True

    else:
        missing_arguments("vertical_profile()", ["da_bwc", "da_wwc"])

    hovertemplate = (
        xaxes_title + ": %{customdata[0]}<br>" + yaxes_title + ": %{customdata[1]:.2f}"
    )

    fig.update_xaxes(title_text=xaxes_title)
    fig.update_yaxes(title_text=yaxes_title)
    fig.update_layout(hovermode="closest", showlegend=True)
    fig.update_traces(hovertemplate=hovertemplate)

    return fig
