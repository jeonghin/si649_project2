import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


layers = ["conv2d5", "conv2d6", "conv2d7", "conv2d8", "conv2d9", "linear1", "linear2"]
color_dict = {
    "ClassifierA_Cr203_C6": "#B3262A",
    "ClassifierA_test_stim": "#2f559a",
    "ClassifierA_test_unstim": "#5AADC5",
}

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(
    [
        html.Div(
            id="plot-container",
            children=[
                html.P(
                    children=[
                        "The original report can be accessed through this ",
                        html.A(
                            "BioRxiv Link",
                            href="https://www.biorxiv.org/content/10.1101/2023.06.01.542416v1.full.pdf",
                            target="_blank",
                        ),
                        " and the data through this ",
                        html.A(
                            "GitHub repository",
                            href="https://github.com/MannLabs/SPARCS_pub_figures",
                            target="_blank",
                        ),
                    ],
                    id="initial-announcement",
                ),
                html.P(
                    "Please select a layer to view from the dropdown.",
                    id="initial-message",
                ),
            ],
        ),
        dcc.Dropdown(
            id="layer-dropdown",
            options=[{"label": layer, "value": layer} for layer in layers],
            value=layers[0],
        ),
        dcc.Graph(id="umap-plot"),
    ]
)


# Callback to update the plot based on dropdown selection
@app.callback(Output("umap-plot", "figure"), [Input("layer-dropdown", "value")])
def update_plot(selected_layer):

    input_path = (
        f"data/classifier_1_Test_Data/UMAP_data/Raw_data_UMAP_{selected_layer}.csv"
    )
    df_train_umap = pd.read_csv(input_path)

    fig = px.scatter(
        df_train_umap.sample(frac=1, random_state=19),
        x="UMAP_1",
        y="UMAP_2",
        color="class_label",
        color_discrete_map=color_dict,
        title=f"UMAP Test Data Labels - {selected_layer}",
    )
    fig.update_traces(
        marker=dict(size=4, opacity=1, line=dict(width=0)),
        selector=dict(mode="markers"),
    )

    # Update layout to have equal aspect ratio
    fig.update_layout(
        xaxis=dict(
            scaleanchor="y",
            scaleratio=1,
            dtick=2,
        ),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            dtick=2,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    # Set a constant range for both axes
    umap_min = min(df_train_umap["UMAP_1"].min(), df_train_umap["UMAP_2"].min())
    umap_max = max(df_train_umap["UMAP_1"].max(), df_train_umap["UMAP_2"].max())

    x_range = [umap_min - 2, umap_max + 2]
    # y_range = [umap_min - 2, umap_max + 2]

    fig.update_xaxes(range=x_range, constrain="domain")
    # fig.update_yaxes(range=y_range, scaleanchor="x", scaleratio=1)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
