import pickle
import altair as alt
import pandas as pd
import panel as pn

pn.extension("vega")

# Read files
with open("data_a.pkl", "rb") as file:
    data_a = pickle.load(file)

with open("data_b.pkl", "rb") as file:
    data_b = pickle.load(file)

with open("data_c.pkl", "rb") as file:
    data_c = pickle.load(file)

with open("BflyAll.pkl", "rb") as file:
    BflyAll = pickle.load(file)

with open("BfObsYr.pkl", "rb") as file:
    BfObsYr = pickle.load(file)

with open("BfObsCv.pkl", "rb") as file:
    BfObsCv = pickle.load(file)

image_pane = pn.pane.PNG('F3_Bfly_GN_Coverage.png', width=800, height=500) 

# Selection widgets 
subgroup_select = pn.widgets.Select(name='Layers', options=["a", "b", "c"])

# Bind the widgets to the create_plot function
@pn.depends(subgroup_select.param.value)
def create_plot(layers):
    

    if layers == "a":
        # Define a single selection that chooses a single piece of data to highlight in the legend.
        single_selection = alt.selection_single(fields=["Source"], bind="legend", empty="all")
        
        # Define the interactive chart
        chart = (
            (
                alt.Chart(data_a)
                .mark_line(point=True)
                .encode(
                    x=alt.X("Year:Q", axis=alt.Axis(title="Year")),
                    y=alt.Y("G:Q", axis=alt.Axis(title="Group Number")),
                    color=alt.Color("Source:N", legend=alt.Legend(title="Source")),
                    strokeDash="Source:N",
                    tooltip=["Year:Q", "G:Q", "Source:N"],
                    opacity=alt.condition(
                        single_selection, alt.value(1), alt.value(0)
                    ),  
                )
                .add_selection(single_selection) 
                .properties(
                    
                    width=1000,  
                )
                .interactive()
            )
            .configure_axis(grid=False)
            .configure_view(strokeWidth=0)
            .configure_point(size=15)
        )
        
      
        return chart
        
    elif layers == "b":
        YrCum = 2
        
        matplotlib_colors = [
            (0.61, 0.38, 0.38),
            (0.65, 0.5, 0.35),
            (0.60, 0.60, 0.4),
            (0.42, 0.5, 0.56),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
        ]
        
        
        def rgb_to_hex(rgb):
            """Converts an RGB tuple in the range (0, 1) to a hexadecimal color code."""
            return "#" + "".join(f"{int(c*255):02x}" for c in rgb)
        
        
        def clr_based_on_BfObsCv(cv):
            """Returns a color based on the coverage value."""
       
            color0 = "A"
            colorsMsk = ["B", "C", "D", "E"]
            if cv == 0:
                return "0%"
            elif cv < 0.05:
                return "<5%"
            elif cv < 0.1:
                return "<10%"
            elif cv < 0.15:
                return "<15%"
            elif cv < 0.2:
                return "20%"
            elif cv < 0.4:
                return "40%"
            elif cv < 0.6:
                return "60%"
            elif cv < 0.8:
                return "80%"
            else:
                return "100%"
                
        def alpha_based_on_BfObsCv(cv):
            """Returns an alpha value based on the coverage value."""
            if cv == 0:
                return MaskMaxAl
            else:
                return max(0.1, MaskMaxAl * (1 - cv))
        
       
        single_selection = alt.selection_single(fields=["Source"], bind="legend", empty="all")
        
        
        chart = (
            alt.Chart(data_a)
            .mark_line()
            .encode(
                x=alt.X("Year:Q", axis=alt.Axis(title="Year")),
                y=alt.Y("G:Q", axis=alt.Axis(title="GN Masked Using Observed Days")),
                tooltip=["Year:Q", "G:Q"],
                opacity=alt.condition(
                    single_selection, alt.value(1), alt.value(0)
                ), 
            )
            .add_selection(single_selection) 
            .properties(
               
                width=1000,  
            )
        )
        
        mask_plot = (
            alt.Chart(data_b)
            .mark_area(
                clip=True,
                interpolate="monotone",
            )
            .encode(
                alt.X("YearStart:Q"),
                alt.Y("Ymax:Q"),
                alt.Color(
                    "Color:N",
                    scale=alt.Scale(
                        domain=[
                            "0%",
                            "<5%",
                            "<10%",
                            "<15%",
                            "20%",
                            "40%",
                            "60%",
                            "80%",
                            "100%",
                        ],
                        range=[rgb_to_hex(color) for color in matplotlib_colors],
                    ),
                ),
                opacity=alt.Opacity("Alpha:Q", legend=None),
                tooltip=[
                    "YearStart:Q",
                    "YearEnd:Q",
                    "Color:N",
                ],
            )
            .interactive()
        )
        
        combined_plot = (mask_plot + chart).properties(
            
            width=1000,
        )
        
        return combined_plot
    else:
      
        MaskMaxAl = 0.8
        
        # Colormap for transparency mask
        matplotlib_colors = [
            (0.61, 0.38, 0.38),
            (0.65, 0.5, 0.35),
            (0.60, 0.60, 0.4),
            (0.42, 0.5, 0.56),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5),
        ]        
        
        def rgb_to_hex(rgb):
            """Converts an RGB tuple in the range (0, 1) to a hexadecimal color code."""
            return "#" + "".join(f"{int(c*255):02x}" for c in rgb)        
        
        def clr_based_on_BfObsCv(cv):
            """Returns a color based on the coverage value."""
            
            color0 = "A"
            colorsMsk = ["B", "C", "D", "E"]
            if cv == 0:
                return "0%"
            elif cv < 0.05:
                return "<5%"
            elif cv < 0.1:
                return "<10%"
            elif cv < 0.15:
                return "<15%"
            elif cv < 0.2:
                return "20%"
            elif cv < 0.4:
                return "40%"
            elif cv < 0.6:
                return "60%"
            elif cv < 0.8:
                return "80%"
            else:
                return "100%"
        
        
        def alpha_based_on_BfObsCv(cv):
            """Returns an alpha value based on the coverage value."""
            if cv == 0:
                return MaskMaxAl
            else:
                return max(0.1, MaskMaxAl * (1 - cv))


        YrCum = 2
    
        mask_df = pd.DataFrame(
            {
                "YearStart": BfObsYr,
                "YearEnd": BfObsYr + YrCum,  
                "Coverage": BfObsCv,
               
                "Color": [clr_based_on_BfObsCv(i) for i in BfObsCv],  
                "Alpha": [alpha_based_on_BfObsCv(i) for i in BfObsCv], 
                "Ymin": -80,
                "Ymax": 80,
            }
        )
        
        
        mask_plot = (
            alt.Chart(data_c)
            .mark_area(
                clip=True,
                interpolate="monotone",
            )
            .encode(
                alt.X("YearStart:Q", title="Year"),
                alt.Y("Ymax:Q", title="Latitude (o)"),
                alt.Color(
                    "Color:N",
                    scale=alt.Scale(
                        domain=[
                            "0%",
                            "<5%",
                            "<10%",
                            "<15%",
                            "20%",
                            "40%",
                            "60%",
                            "80%",
                            "100%",
                        ],
                        range=[rgb_to_hex(color) for color in matplotlib_colors],
                    ),
                ),
                opacity="Alpha:Q",
                tooltip=[
                    "YearStart:Q",
                    "YearEnd:Q",
                    "Color:N",
                ],
            )
            .interactive()
        )
        
        mask_plot2 = (
            alt.Chart(data_c)
            .mark_area(
                clip=True,
                interpolate="monotone",
            )
            .encode(
                alt.X("YearStart:Q", title="Year"),
                alt.Y("Ymin:Q", title="Latitude (o)"),
                alt.Color(
                    "Color:N",
                    scale=alt.Scale(
                        domain=[
                            "0%",
                            "<5%",
                            "<10%",
                            "<15%",
                            "20%",
                            "40%",
                            "60%",
                            "80%",
                            "100%",
                        ],
                        range=[rgb_to_hex(color) for color in matplotlib_colors],
                    ),
                ),
                opacity="Alpha:Q",
                tooltip=[
                    "YearStart:Q",
                    "YearEnd:Q",
                    "Color:N",
                ],
            )
            .interactive()
        )
        
        BflyAll_sample = BflyAll.sample(n=5000, random_state=19)
        
        # Scatter plot
        scatter_plot = (
            alt.Chart(BflyAll_sample)
            .mark_point(opacity=0.3, color="black")
            .encode(
                x=alt.X("FRACYEAR:Q", title="Year"), 
                y=alt.Y("LATITUDE:Q", title="Latitude (o)"), 
            )
        )
        
        # Combine plots
        combined_plot = (mask_plot2 + mask_plot + scatter_plot).properties(
            width=1000,
        )

        return combined_plot

# Main layout
main_layout = pn.Column(
    "# Data Interactive Visualization (NatAs_SN_Perspective)",
    image_pane,
    subgroup_select,
    pn.panel(create_plot, reactive=True),

)

# Create a basic template
template = pn.template.BootstrapTemplate(title='SI649 Project 2')
template.main.append(main_layout)

# Serve the application
template.servable()
