import altair as alt
import pandas as pd
import panel as pn

pn.extension('vega')

# Selection widgets 1
subgroup_select1 = pn.widgets.Select(name='Layers', options=["conv2d5", "conv2d6", "conv2d7", "conv2d8", "conv2d9", "linear1", "linear2"])
# Selection widgets 2
subgroup_select2 = pn.widgets.Select(name='Layers', options=["conv2d5", "conv2d6", "conv2d7", "conv2d8", "conv2d9", "linear1", "linear2"])

# Bind the widgets to the create_plot function
def create_plot(subgroup_select):
    @pn.depends(subgroup_select.param.value)
    def _plot(layers):
        df_train_umap = pd.read_csv(f"https://raw.githubusercontent.com/jeonghin/si649_project2/main/data/classifier_1_Test_Data/UMAP_data/Raw_data_UMAP_{layers}.csv").sample(n=5000, random_state=19)
        color_dict = {
            "ClassifierA_Cr203_C6": "#B3262A",
            "ClassifierA_test_stim": "#2f559a",
            "ClassifierA_test_unstim": "#5AADC5",
        }
    
        # Define a selection for zooming and panning (interval)
        zoom = alt.selection_interval(bind='scales')
    
        # Define a selection for the legend
        legend_selection = alt.selection_multi(fields=['class_label'], bind='legend')
    
    
        # Create the Altair chart object
        chart = alt.Chart(df_train_umap).mark_circle(size=4, opacity=1).encode(
            x=alt.X("UMAP_1:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("UMAP_2:Q", scale=alt.Scale(zero=False)),
            color=alt.Color("class_label:N", scale=alt.Scale(domain=list(color_dict.keys()), range=list(color_dict.values()))),
            tooltip=['UMAP_1', 'UMAP_2', 'class_label'],
            opacity=alt.condition(legend_selection, alt.value(1), alt.value(0))  # Use the selection here to control opacity
        ).properties(
            title=f"UMAP Test Data Labels - {layers}",
        ).add_selection(
            legend_selection,  # Add the selection to the chart
        
            zoom
        ).configure_axis(
            grid=False
        ).configure_view(
            strokeWidth=0
        )
    
        return chart
    return _plot
    
    # # Combine everything in a Panel Column to create an app
    # app = pn.Column("# UMAP Data Interactive Visualization", subgroup_select, pn.panel(create_plot, reactive=True))
    
    # # Set the app to be servable
    # app.servable()
    
    # Create two instances of the main layout
    # Main layout 1
main_layout1 = pn.Column(
    "# Data Interactive Visualization (SPARCS)",
    subgroup_select1,
    pn.panel(create_plot(subgroup_select1), reactive=True),
)

# Main layout 2
main_layout2 = pn.Column(
    "# Data Interactive Visualization (SPARCS)",
    subgroup_select2,
    pn.panel(create_plot(subgroup_select2), reactive=True),
)

# Place layouts side by side using pn.Row
side_by_side_layout = pn.Row(main_layout1, main_layout2)

# Create a basic template
template = pn.template.BootstrapTemplate(title='SI649 Project 2')
template.main.append(side_by_side_layout)

# Serve the application
template.servable()
