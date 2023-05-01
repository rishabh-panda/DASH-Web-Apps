from heapq import merge
import uuid
from turtle import color
import dash
from dash import dash_table
from dash import dcc, html
import pyodbc
import base64
from dash import Input, Output, callback, State
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import pandas as pd
import dash_draggable as draggable

app = dash.Dash(__name__)

dash.register_page(__name__,
                   path='/scenario-modeling-dashboard',
                   title='Scenario modeling tool',
                   name='Scenario modeling tool'
)

cnxn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};",
    "SERVER=aag-a7rw-sql-server.database.windows.net;",
    "DATABASE=product_testing;",
    "Trusted_Connection=yes;",
    "UID=;",
    "PWD=;",
)

cnxn_str = ";".join(cnxn_str)

# Establish connection with SQL server
cnxn = pyodbc.connect(cnxn_str)

suppliers = ["Supplier A", "Supplier B", "Supplier C", "Supplier F", "Own Brand"]
df_sku_action = pd.read_sql(
    "SELECT top 100 * FROM testing.abs_cereals_sku_action_dash", cnxn
)
df_sku_action = df_sku_action[df_sku_action["Group_Supplier_Name"].isin(suppliers)]
df_loyalty_substitution = pd.read_sql(
    "SELECT * FROM testing.abs_cereals_loyalty_substitution_dash", cnxn
)
df_loyalty_substitution = df_loyalty_substitution[
    df_loyalty_substitution["Group_Supplier_Name"].isin(suppliers)
]

# Perform inner join on specified keys
merged_df = pd.merge(
    df_sku_action,
    df_loyalty_substitution,
    left_on=[
        "SKU_ID",
        "SKU_Name",
        "Brand_Name",
        "Group_Supplier_Name",
        "Level_1_Name",
        "Level_2_Name",
        "Level_3_Name",
        "Level_4_Name",
        "CDT_Level_2",
    ],
    right_on=[
        "SKU_ID",
        "SKU_Name",
        "Brand_Name",
        "Group_Supplier_Name",
        "Level_1_Name",
        "Level_2_Name",
        "Level_3_Name",
        "Level_4_Name",
        "CDT_Level_1",
    ],
    how="inner",
)

# Perform inner join on specified keys
merged_df = pd.merge(
    df_sku_action,
    df_loyalty_substitution,
    on=[
        "SKU_ID",
        "SKU_Name",
        "Brand_Name",
        "Group_Supplier_Name",
        "Level_1_Name",
        "Level_2_Name",
        "Level_3_Name",
        "Level_4_Name",
    ],
    how="inner",
    suffixes=("", "_y"),
).loc[:, ~merged_df.columns.str.endswith("_y")]

df = merged_df
# df = pd.read_csv("abs_cereals_sku_action_dash.csv")

df.dropna(how="all", axis=1, inplace=True)

# rename the columns
df = df.rename(
    columns={
        "Overall_Sales": "Overall sales",
        "Level_1_Name": "Category group",
        "Level_2_Name": "Category",
        "Level_3_Name": "Sub-category",
        "Brand_Name": "Brand name",
        "SKU_Name": "Item",
        "Sales": "Sales numeric",
        "Loyalty": "Loyalty numeric",
        "Substitution": "Substitution numeric",
        "Sales_at_Risk": "Sales",
        "Transferable_Sales": "Transferable sales numeric",
        "Group_Supplier_Name": "Supplier",
    }
)

# access the required columns
df = df[
    [
        "Item",
        "Sub-category",
        "Category",
        "Category group",
        "Supplier",
        "Brand name",
        "Sales numeric",
        "Volume",
        "TNP",
        "Loyalty numeric",
        "Substitution numeric",
        "Sales",
        "Transferable sales numeric",
        "Overall sales",
    ]
]

# converting Overall sales to millions
df["Overall sales"] = df["Overall sales"] / pow(10, 6)
df["Overall sales"] = df["Overall sales"].round(2)
df["Overall sales"] = "$" + df["Overall sales"].astype(str) + "M"

# converting Sales at risk to millions
df["Sales"] = df["Sales"] / pow(10, 6)
df["Sales"] = df["Sales"].round(2)
df["Sales"] = "$" + df["Sales"].astype(str) + "M"

# converting Transferable sales to millions
df["Transferable sales"] = df["Transferable sales numeric"] / pow(10, 6)
df["Transferable sales"] = df["Transferable sales"].round(2)
df["Transferable sales"] = "$" + df["Transferable sales"].astype(str) + "M"

# converting Sales numeric to millions
df["Sales numeric"] = df["Sales numeric"] / pow(10, 6)
df["Sales numeric"] = df["Sales numeric"].round(2)

# converting Transferable sales numeric to millions
df["Transferable sales numeric"] = df["Transferable sales numeric"] / pow(10, 6)
df["Transferable sales numeric"] = df["Transferable sales numeric"].round(2)

# Rounding off Loyalty numeric
df["Loyalty numeric"] = df["Loyalty numeric"].round(3)

# Rounding off Substitution numeric
df["Substitution numeric"] = df["Substitution numeric"].round(3)

# converting TNP to millions
df["TNP"] = df["TNP"] / pow(10, 6)
df["TNP"] = df["TNP"].round(2)
df["TNP"] = "$" + df["TNP"].astype(str) + "M"

# converting Loyalty to percentage
df["Loyalty"] = df["Loyalty numeric"] * 100
df["Loyalty"] = df["Loyalty"].round(2)
df["Loyalty"] = df["Loyalty"].astype(str) + "%"

# converting Substitution to percentage
df["Substitution"] = df["Substitution numeric"] * 100
df["Substitution"] = df["Substitution"].round(2)
df["Substitution"] = df["Substitution"].astype(str) + "%"

# converting Volume to thousands
df["Volume"] = df["Volume"] / pow(10, 3)
df["Volume"] = df["Volume"].round(2)
df["Volume"] = df["Volume"].astype(str) + "K"

df = (
    df.groupby(
        [
            "Item",
            "Sub-category",
            "Category",
            "Category group",
            "Supplier",
            "Brand name",
            "Volume",
            "TNP",
            "Loyalty",
            "Substitution",
            "Sales",
            "Transferable sales",
            "Overall sales",
        ]
    )[
        "Sales numeric",
        "Loyalty numeric",
        "Substitution numeric",
        "Transferable sales numeric",
    ]
    .sum()
    .reset_index()
)

# save the Merchant Accelerator logo in a variable
ma_logo_png = r"./Assets/MA logo red.png"
ma_logo_base64 = base64.b64encode(open(ma_logo_png, "rb").read()).decode("ascii")

# save the Home logo in a variable
home_logo_png = r"./Assets/home.png"
home_logo_base64 = base64.b64encode(open(home_logo_png, "rb").read()).decode("ascii")

# save the Info logo in a variable
info_logo_png = r"./Assets/info.png"
info_logo_base64 = base64.b64encode(open(info_logo_png, "rb").read()).decode("ascii")

# define the color scheme
colors = {"background": "white", "text": "rgb(51,51,51)"}

# create dropdown components
category_group_dropdown = dcc.Dropdown(
    id="category-group-dropdown-sm",
    options=df["Category group"].unique(),
    placeholder="(All)",
    multi=True,
    style={
        "backgroundColor": colors["background"],
        "color": colors["text"],
        "margin": "10px 0px 0px 0px",
    },
    className="gray-pill",
)

category_dropdown = dcc.Dropdown(
    id="category-dropdown-sm",
    options=df["Category"].unique(),
    placeholder="(All)",
    multi=True,
    style={
        "backgroundColor": colors["background"],
        "color": colors["text"],
        "margin": "10px 0px 0px 0px",
    },
    className="gray-pill",
)

sub_category_dropdown = dcc.Dropdown(
    id="sub-category-dropdown-sm",
    options=df["Sub-category"].unique(),
    placeholder="(All)",
    multi=True,
    style={
        "backgroundColor": colors["background"],
        "color": colors["text"],
        "margin": "10px 0px 0px 0px",
    },
    className="gray-pill",
)

Supplier_dropdown = dcc.Dropdown(
    id="Supplier-dropdown-sm",
    options=df["Supplier"].unique(),
    placeholder="(All)",
    multi=True,
    style={
        "backgroundColor": colors["background"],
        "color": colors["text"],
        "margin": "10px 0px 0px 0px",
    },
    className="gray-pill",
)

brand_dropdown = dcc.Dropdown(
    id="brand-dropdown-sm",
    options=df["Brand name"].unique(),
    placeholder="(All)",
    multi=True,
    style={
        "backgroundColor": colors["background"],
        "color": colors["text"],
        "margin": "10px 0px 0px 0px",
    },
    className="gray-pill",
)

item_dropdown = dcc.Dropdown(
    id="item-dropdown-sm",
    options=df["Item"].unique(),
    placeholder="(All)",
    multi=True,
    style={
        "backgroundColor": colors["background"],
        "color": colors["text"],
        "margin": "10px 0px 0px 0px",
    },
    className="gray-pill",
)

sales_range_slider = dcc.RangeSlider(
    id="sales-slider",
    min=df["Sales numeric"].min(),
    max=df["Sales numeric"].max(),
    marks=None,
)

selected_scenarios = []

loyalty_range_slider = dcc.RangeSlider(
    id="loyalty-slider",
    min=df["Loyalty numeric"].min(),
    max=df["Loyalty numeric"].max(),
    marks=None,
)

substitution_range_slider = dcc.RangeSlider(
    id="substitution-slider",
    min=df["Substitution numeric"].min(),
    max=df["Substitution numeric"].max(),
    marks=None,
)

app = dash.Dash(__name__)

# # Define the options for the checkboxes
checkbox_options = [{"value": "unchecked"}]

# Define the layout of the app
layout = html.Div(
    [
        html.Div(
            [
                # Heading
                html.H1(
                    "Scenario modeling tool",
                    style={
                        "display": "inline-block",
                        "color": "rgb(204, 0, 0)",
                        "height": "80px",
                        "font-weight": "bold",
                        "margin-left": "35px",
                        "margin-bottom": "-0.2px",
                        "fontSize": 27,
                        "font-family": "Arial",
                    },
                ),
                # Merchant Accelerator Logo
                html.Img(
                    src="data:image/png;base64,{}".format(ma_logo_base64),
                    style={
                        "width": "350px",
                        "height": "auto",
                        "margin-left": "1400px",
                        "margin-right": "200px",
                        "margin-top": "-70px",
                        "margin-bottom": "10px",
                        "float": "right",
                    },
                ),
                # Home Logo
                html.A(
                    html.Img(
                        src="data:image/png;base64,{}".format(home_logo_base64),
                        style={
                            "width": "30px",
                            "height": "auto",
                            "margin-left": "1000px",
                            "margin-right": "130px",
                            "margin-top": "-72px",
                            "margin-bottom": "10px",
                            "float": "right",
                        },
                    ),
                    href="http://localhost:8050",
                ),
                # Info Logo
                html.Img(
                    src="data:image/png;base64,{}".format(info_logo_base64),
                    style={
                        "width": "34px",
                        "height": "auto",
                        "margin-left": "100px",
                        "margin-right": "60px",
                        "margin-top": "-72px",
                        "margin-bottom": "10px",
                        "float": "right",
                    },
                    title="Note:\n1) All figures are based on data for Financial Year 2021\n\nSource: RetailCo's financial data",
                ),
            ]
        ),
        html.Div(
            [
                # Sub-heading
                html.H4(
                    "What will be the impact of adding/delisting items from a supplier?",
                    style={
                        "display": "flex",
                        "justify-content": "space-between",
                        "margin-left": "35px",
                        "margin-top": "-50px",
                        "font-weight": "normal",
                        "fontSize": 18,
                        "color": colors["text"],
                        "font-family": "Arial",
                    },
                ),
            ]
        ),
        # Gray bar denoting: 'Assortment planning ❯ Planning review'
        html.Div(
            [
                html.Span(
                    "Assortment planning  ❯", style={"color": "rgb(170, 170, 170)"}
                ),
                html.Span("  Planning review", style={"color": "rgb(51, 51, 51)"}),
            ],
            style={
                "background-color": "rgb(226,226,226)",
                "text-align": "left",
                "height": "30px",
                "width": "1808px",
                "margin-left": "35px",
                "margin-right": "0px",
                "fontSize": 15,
                "font-family": "Arial",
                "padding-top": "10px",
                "padding-bottom": "2px",
                "padding-left": "10px",
                "white-space": "nowrap",
            },
        ),
        # Dropdowns
        html.Div(
            [
                html.Div(
                    [html.Label("Category group"), category_group_dropdown],
                    style={
                        "width": "15%",
                        "display": "inline-block",
                        "margin-left": "24px",
                        "margin-top": "25px",
                        "margin-bottom": "21px",
                        "border-right": "1px solid lightgray",
                        "padding": "10px",
                        "fontSize": 15,
                        "font-family": "Arial",
                    },
                ),
                html.Div(
                    [html.Label("Category"), category_dropdown],
                    style={
                        "width": "15%",
                        "display": "inline-block",
                        "border-right": "1px solid lightgray",
                        "padding": "10px",
                        "fontSize": 15,
                        "font-family": "Arial",
                    },
                ),
                html.Div(
                    [html.Label("Sub-category"), sub_category_dropdown],
                    style={
                        "width": "15%",
                        "display": "inline-block",
                        "border-right": "1px solid lightgray",
                        "padding": "10px",
                        "fontSize": 15,
                        "font-family": "Arial",
                    },
                ),
                html.Div(
                    [html.Label("Supplier"), Supplier_dropdown],
                    style={
                        "width": "15%",
                        "display": "inline-block",
                        "border-right": "1px solid lightgray",
                        "padding": "10px",
                        "fontSize": 15,
                        "font-family": "Arial",
                    },
                ),
                html.Div(
                    [html.Label("Brand"), brand_dropdown],
                    style={
                        "width": "15%",
                        "display": "inline-block",
                        "border-right": "1px solid lightgray",
                        "padding": "10px",
                        "fontSize": 15,
                        "font-family": "Arial",
                    },
                ),
                html.Div(
                    [html.Label("Item"), item_dropdown],
                    style={
                        "width": "15%",
                        "display": "inline-block",
                        "margin-left": "10px",
                        "fontSize": 15,
                        "font-family": "Arial",
                    },
                ),
            ]
        ),
        # range sliders
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "Sales (in $M)",
                            style={
                                "align-self": "center",
                                "margin-bottom": "5px",
                                "font-family": "Arial",
                                "fontSize": 15,
                            },
                        ),
                        dcc.RangeSlider(
                            id="sales-slider",
                            min=df["Sales numeric"].min(),
                            max=df["Sales numeric"].max(),
                            value=[
                                df["Sales numeric"].min(),
                                df["Sales numeric"].max(),
                            ],
                            step=df["Sales numeric"].min(),
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                            },
                            marks=None,
                        ),
                    ],
                    style={
                        "width": "33%",
                        "display": "flex",
                        "flex-direction": "column",
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "Loyalty (in %)",
                            style={
                                "align-self": "center",
                                "margin-bottom": "5px",
                                "font-family": "Arial",
                                "fontSize": 15,
                            },
                        ),
                        dcc.RangeSlider(
                            id="loyalty-slider",
                            min=0,
                            max=100,
                            value=[
                                0,
                                100,
                            ],
                            step=(df["Loyalty numeric"]*100).min(),
                            tooltip={"placement": "bottom", "always_visible": True},
                            marks=None,
                        ),
                    ],
                    style={
                        "width": "33%",
                        "display": "flex",
                        "flex-direction": "column",
                    },
                ),
                html.Div(
                    [
                        html.Label(
                            "Substitution (in %)",
                            style={
                                "align-self": "center",
                                "margin-bottom": "5px",
                                "font-family": "Arial",
                                "fontSize": 15,
                            },
                        ),
                        dcc.RangeSlider(
                            id="substitution-slider",
                            min=0,
                            max=100,
                            value=[
                                0,
                                100,
                            ],
                            step=(df["Substitution numeric"]*100).min(),
                            tooltip={"placement": "bottom", "always_visible": True},
                            marks=None,
                        ),
                    ],
                    style={
                        "width": "33%",
                        "display": "flex",
                        "flex-direction": "column",
                    },
                ),
            ],
            style={"display": "flex", "flex-direction": "row", "margin-bottom": "20px"},
        ),
        # master datatable
        html.Div(
            [
                dash_table.DataTable(
                    id="datatable-interactivity",
                    columns=[
                        {"name": i, "id": i}
                        for i in df.columns
                        if i
                        not in [
                            "Sales numeric",
                            "Loyalty numeric",
                            "Substitution numeric",
                            "Transferable sales numeric",
                        ]
                    ],
                    data=df.to_dict("rows"),
                    editable=False,
                    row_selectable="multi",
                    selected_rows=[],
                    style_data_conditional=[
                        {
                            "if": {"column_id": "Sales"},
                            "backgroundColor": "rgb(222, 220, 220)",
                        },
                        {
                            "if": {"column_id": "TNP"},
                            "backgroundColor": "rgb(222, 220, 220)",
                        },
                        {
                            "if": {"column_id": "Transferable sales"},
                            "backgroundColor": "rgb(222, 220, 220)",
                        },
                        {
                            "if": {"column_id": "Overall sales"},
                            "backgroundColor": "rgb(222, 220, 220)",
                        },
                    ],
                    style_header={
                        "backgroundColor": "rgb(204,0,0)",
                        "fontWeight": "bold",
                        "color": "white",
                        "fontSize": 15,
                        "font-family": "Arial",
                        ".multi-select-dropdown": {
                            "background-color": "black",
                            "color": "white",
                        },
                    },
                    style_table={
                        "backgroundColor": "white",
                        "overflowX": "scroll",
                        "overflowY": "scroll",
                        "fontSize": 15.4,
                        "padding-left": "34px",
                        "height": "40vh",
                        "width": "188vh",
                        "font-family": "Arial",
                        "margin": {"l": 40, "r": 40, "t": 40, "b": 40},
                    },
                    style_cell={
                        "width": "100px",
                        "textAlign": "left",
                        "backgroundColor": "white",
                        "font-family": "Arial",
                        "font-size": "0.88em",
                    },
                )
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H3(
                                                    "Create a new scenario",
                                                    style={
                                                        "font-family": "Arial, Helvetica, sans-serif",
                                                        "color": "rgb(204, 0, 0)",
                                                    },
                                                ),
                                                dcc.Input(
                                                    id="scenario_name",
                                                    type="text",
                                                    placeholder="Scenario name",
                                                    style={
                                                        "border": "none",
                                                        "font-size": "medium",
                                                        "border-bottom": "1px solid grey",
                                                        "box-sizing": "border-box",
                                                        "padding": "2px",
                                                        "margin-bottom": "5px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "align-items": "center",
                                                "justify-content": "space-between",
                                            },
                                        ),
                                        dash_table.DataTable(
                                            id="display_selected_row_data_table1",
                                            columns=[
                                                {"name": i, "id": i}
                                                for i in df.columns
                                                if i
                                                not in [
                                                    "Sales numeric",
                                                    "Loyalty numeric",
                                                    "Substitution numeric",
                                                    "Transferable sales numeric",
                                                    "Transferable sales",
                                                    "TNP",
                                                    "Volume",
                                                    "Category group",
                                                ]
                                            ],
                                            data=[],
                                            style_header={
                                                "backgroundColor": "rgb(226,226,226)",
                                                "fontWeight": "bold",
                                                "color": "black",
                                                "fontSize": 15,
                                                "font-family": "Arial",
                                                ".multi-select-dropdown": {
                                                    "background-color": "black",
                                                    "color": "white",
                                                },
                                            },
                                            style_table={
                                                "backgroundColor": "white",
                                                # "overflowY": "scroll",
                                                "fontSize": 15.4,
                                                "height": "30vh",
                                                "font-family": "Arial",
                                                "margin": {
                                                    "l": 40,
                                                    "r": 40,
                                                    "t": 40,
                                                    "b": 40,
                                                },
                                            },
                                            style_cell={
                                                "width": "50vw",
                                                "flex-direction": "row",
                                                "textAlign": "left",
                                                "backgroundColor": "white",
                                                "font-family": "Arial",
                                                "font-size": "0.88em",
                                            },
                                        ),
                                        html.Br(),
                                        html.Div(
                                            [
                                                html.Button(
                                                    "Save Scenario",
                                                    id="save_scenario",
                                                    n_clicks=0,
                                                    style={
                                                        "style": "none",
                                                        "background": "rgb(204, 0, 0)",
                                                        "padding": "10px",
                                                        "color": "white",
                                                        "border": "none",
                                                        "width": "200px",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                                html.Button(
                                                    "Update",
                                                    id="update_table",
                                                    n_clicks=0,
                                                    style={
                                                        "style": "none",
                                                        "background": "grey",
                                                        "padding": "10px",
                                                        "color": "white",
                                                        "border": "none",
                                                        "width": "200px",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "justify-content": "space-between",
                                                "margin-bottom": "20px",
                                            },
                                        ),
                                        html.Div(id="data_saved"),
                                    ]
                                ),
                            ],
                            style={"width": "50vw"},
                        ),
                        html.Div(
                            [
                                html.H3(
                                    "Impact on Suppliers - Preview",
                                    style={"font-family": "Arial"},
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            id="scenario",
                                            style={
                                                "font-weight": "bold",
                                                "font-family": "Arial",
                                                "margin-right": "10px",
                                            },
                                        ),
                                        html.Div(id="1-sales-chart"),
                                        html.Div(
                                            id="1-transferable-sales-chart",
                                            style={"margin-left": "-50px"},
                                        ),
                                        html.Div(
                                            id="1-total-impact-chart",
                                            style={"margin-left": "-50px"},
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "width": "100%",
                                        "justify-content": "center",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "align-items": "center",
                                "background": "whitesmoke",
                                "padding": "10px",
                                "border-radius": "6px",
                                "margin": "10px",
                                "width": "45vw",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "align-items": "center",
                        "justify-content": "center",
                    },
                ),
            ],
            style={
                "margin-top": "20px",
                "display": "flex",
                "flex-direction": "row",
                "padding": "10px 30px",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H2("All scenarios"),
                                html.Button(
                                    "Refresh",
                                    id="all_scenarios_btn",
                                    n_clicks=0,
                                    style={
                                        "style": "none",
                                        "padding": "6px",
                                        "margin-left": "10px",
                                        "height": "30px",
                                        "border": "none",
                                        "background": "rgb(204,0,0)",
                                        "color": "white",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "row",
                                "align-items": "center",
                            },
                        ),
                        html.Div(id="all_scenarios"),
                    ],
                    style={
                        "width": "100%",
                    },
                ),
                html.Div(
                    [html.H2("Selected scenarios"), html.Div(id="selected_scenarios")],
                    style={
                        "width": "100%",
                        "height": "100%",
                        "padding-left": "15px",
                        "background": "white",
                        "border-radius": "8px",
                    },
                ),
            ],
            style={
                "font-family": "Arial",
                "display": "flex",
                "flex-direction": "row",
                "justify-content": "space-between",
                "align-items": "flex-start",
                "margin": "2rem",
                "height": "20vh",
                "font-size": "large",
                "padding": "15px 20px",
                "background": "whitesmoke",
                "border-radius": "8px",
            },
        ),
        html.Br(),
        html.Div(
            id="scenario_charts",
            style={
                "display": "flex",
                "flex-direction": "row",
                "width": "100vw",
                "overflow-x": "scroll",
            },
        ),
    ],
)


@callback(
    Output("datatable-interactivity", "data"),
    [
        Input("category-group-dropdown-sm", "value"),
        Input("category-dropdown-sm", "value"),
        Input("sub-category-dropdown-sm", "value"),
        Input("Supplier-dropdown-sm", "value"),
        Input("brand-dropdown-sm", "value"),
        Input("item-dropdown-sm", "value"),
        Input("sales-slider", "value"),
        Input("loyalty-slider", "value"),
        Input("substitution-slider", "value"),
    ],
    [State("datatable-interactivity", "data")],
)
def update_master_datatable(
    category_group,
    category,
    sub_category,
    Supplier,
    brand,
    item,
    sales_range,
    loyalty_range,
    substitution_range,
    current_data,
):
    # filter the dataframe based on the selected values
    dff = df

    if category_group:
        dff = dff[dff["Category group"].isin(category_group)]

    if category:
        dff = dff[dff["Category"].isin(category)]

    if sub_category:
        dff = dff[dff["Sub-category"].isin(sub_category)]

    if Supplier:
        dff = dff[dff["Supplier"].isin(Supplier)]

    if brand:
        dff = dff[dff["Brand name"].isin(brand)]

    if item:
        dff = dff[dff["Item"].isin(item)]

    filtered_df = dff[
        (dff["Sales numeric"] >= sales_range[0])
        & (dff["Sales numeric"] <= sales_range[1])
        & (dff["Loyalty numeric"] >= loyalty_range[0])
        & (dff["Loyalty numeric"] <= loyalty_range[1])
        & (dff["Substitution numeric"] >= substitution_range[0])
        & (dff["Substitution numeric"] <= substitution_range[1])
    ]

    # check if there are any changes to the data
    if filtered_df.equals(pd.DataFrame(current_data)):
        return current_data.to_dict("records")

    # return the filtered dataframe as a dictionary
    return filtered_df.to_dict("records")


# Define the color scheme
colors = {
    "Supplier A": "rgb(45,71,90)",
    "Supplier B": "rgb(70,100,123)",
    "Supplier C": "rgb(163,188,211)",
    "Supplier F": "rgb(206,155,65)",
    "Own Brand": "rgb(27,163,198)",
    "Supplier G": "rgb(238,178,74)",
}


# Define the callback functions to update each of the tables
@callback(
    Output("display_selected_row_data_table1", "data"),
    Output("scenario", "children"),
    Output("1-sales-chart", "children"),
    Output("1-transferable-sales-chart", "children"),
    Output("1-total-impact-chart", "children"),
    Input("update_table", "n_clicks"),
    State("scenario_name", "value"),
    State("datatable-interactivity", "selected_rows"),
    State("datatable-interactivity", "data"),
)
def update_table1(update_clicks, scenario_name, selected_rows, rows):
    if not selected_rows:
        return [], None

    if update_clicks < 0:
        return [], None

    dff = pd.DataFrame(rows)
    dff = dff.iloc[selected_rows]

    dff["Sales numeric"] = dff["Sales numeric"] * (-1)

    dff["Total impact"] = dff["Transferable sales numeric"] + dff["Sales numeric"]

    dff_grouped = (
        dff.groupby("Supplier")[
            "Sales numeric", "Transferable sales numeric", "Total impact"
        ]
        .sum()
        .reset_index()
    )

    dff_grouped["Supplier_2"] = "All Suppliers"

    fig1 = px.bar(
        dff_grouped,
        x="Supplier_2",
        y="Sales numeric",
        color="Supplier",
        barmode="stack",
        color_discrete_map=colors,
    )
    fig2 = px.bar(
        dff_grouped,
        x="Supplier_2",
        y="Transferable sales numeric",
        color="Supplier",
        barmode="stack",
        color_discrete_map=colors,
    )
    fig3 = px.bar(
        dff_grouped,
        x="Supplier_2",
        y="Total impact",
        color="Supplier",
        barmode="stack",
        color_discrete_map=colors,
    )

    fig1.update_layout(
        title={
            "text": "Delisted sales",
            "font": {"family": "Arial", "size": 14},
            "x": 0.5,
        },
        hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    )

    fig2.update_layout(
        title={
            "text": "Transferable Sales",
            "font": {"family": "Arial", "size": 14},
            "x": 0.5,
        },
        hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    )

    fig3.update_layout(
        title={
            "text": "Total Impact",
            "font": {"family": "Arial", "size": 14},
            "x": 0.25,
        },
        hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    )

    fig1.update_traces(hovertemplate="Sales: $%{y:,.2f}M<br>" "<extra></extra>")

    fig2.update_traces(hovertemplate="Sales: $%{y:,.2f}M<br>" "<extra></extra>")

    fig3.update_traces(hovertemplate="Sales: $%{y:,.2f}M<br>" "<extra></extra>")

    # Set the width and legend of the figures
    fig1.update_layout(width=220, showlegend=False)
    fig2.update_layout(width=220, showlegend=False)
    fig3.update_layout(
        width=220, legend={"title": "", "x": 2.5, "bgcolor": "rgba(0,0,0,0)"}
    )

    fig1.update_yaxes(tickprefix="$", ticksuffix="M")
    fig2.update_yaxes(tickprefix="$", ticksuffix="M")
    fig3.update_yaxes(tickprefix="$", ticksuffix="M")

    fig1.update_layout(xaxis={"showticklabels": False})
    fig2.update_layout(xaxis={"showticklabels": False})
    fig3.update_layout(xaxis={"showticklabels": False})

    # Remove the x-axis and y-axis labels from the figures
    fig1.update_xaxes(title_text="")
    fig1.update_yaxes(title_text="")
    fig2.update_xaxes(title_text="")
    fig2.update_yaxes(title_text="")
    fig3.update_xaxes(title_text="")
    fig3.update_yaxes(title_text="")

    # Set the background color of the figures to white
    fig1.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    return (
        dff.to_dict("records"),
        scenario_name,
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
        dcc.Graph(figure=fig3),
    )


@callback(
    Output("data_saved", "children"),
    Input("save_scenario", "n_clicks"),
    State("scenario_name", "value"),
    State("datatable-interactivity", "selected_rows"),
)
def save_btn(n_clicks, scenario_name, selected_rows):
    if n_clicks > 0:
        # print("Save button clicked")

        # Writeback operation
        cursor = cnxn.cursor()
        uid = uuid.uuid4()
        selected_indexes = ",".join([str(elem) for elem in selected_rows])
        print(selected_indexes)
        cursor.execute(
            """
            INSERT INTO scenario (scenario_id, scenario_name, selected_rows)
            VALUES (?, ?, ?)
            """,
            (uid, scenario_name, selected_indexes),
        )
        cnxn.commit()
        print(scenario_name)
        # print(selected_indexes)
        return "Your scenario is now saved. Please refresh below!"


@callback(
    Output("all_scenarios", "children"),
    # Output("selected_scenarios","children"),
    Input("all_scenarios_btn", "n_clicks"),
)
def scenarios(n_clicks):
    if n_clicks < 0:
        return [], None
    cursor = cnxn.cursor()
    cursor.execute(
        """
            SELECT * FROM scenario
            """,
    )
    rows = cursor.fetchall()
    all_scenarios = []

    for row in rows:
        all_scenarios.append({"id": row.scenario_id, "name": row.scenario_name})
    cnxn.commit()
    return dcc.Checklist(
        [i["name"] for i in all_scenarios],
        id="all_list",
        labelStyle={
            "margin": "10px",
            "font-size": "large",
        },
        style={
            "display": "flex",
            "flex-direction": "row",
        },
    )


@callback(Output("selected_scenarios", "children"), Input("all_list", "value"))
def selected_scenarios_checklist(value):
    return html.Ul(
        [
            html.Li(
                i,
                style={
                    "border-left": "4px solid rgb(204,0,0)",
                    "padding-left": "10px",
                    "margin": "10px",
                    "font-size": "large",
                },
            )
            for i in value
        ],
        id="selected_list",
        style={
            "list-style": "none",
            "display": "flex",
            "flex-direction": "row",
        },
    )


@callback(
    Output("scenario_charts", "children"),
    Input("selected_list", "children"),
    State("datatable-interactivity", "data"),
)
def update_scenario_charts(children, data):
    cursor = cnxn.cursor()
    scenario_data = []
    for i in children:
        print(i)
        cursor.execute(
            """
            SELECT selected_rows,scenario_name FROM scenario where scenario_name=?
            """,
            (i["props"]["children"]),
        )
        row = cursor.fetchone()
        scenario_data.append([list(map(int, row[0].split(","))), row[1]])
        cnxn.commit()
    return [update_scenario_charts(i[1], i[0], data) for i in scenario_data]


def update_scenario_charts(scenario_name, selected_rows, data):
    dff = pd.DataFrame(data)
    dff = dff.iloc[selected_rows]

    dff["Sales numeric"] = dff["Sales numeric"] * (-1)

    dff["Total impact"] = dff["Transferable sales numeric"] + dff["Sales numeric"]

    dff_grouped = (
        dff.groupby("Supplier")[
            "Sales numeric", "Transferable sales numeric", "Total impact"
        ]
        .sum()
        .reset_index()
    )

    dff_grouped["Supplier_2"] = "All Suppliers"

    fig1 = px.bar(
        dff_grouped,
        x="Supplier_2",
        y="Sales numeric",
        color="Supplier",
        barmode="stack",
        color_discrete_map=colors,
    )
    fig2 = px.bar(
        dff_grouped,
        x="Supplier_2",
        y="Transferable sales numeric",
        color="Supplier",
        barmode="stack",
        color_discrete_map=colors,
    )
    fig3 = px.bar(
        dff_grouped,
        x="Supplier_2",
        y="Total impact",
        color="Supplier",
        barmode="stack",
        color_discrete_map=colors,
    )

    fig1.update_layout(
        title={
            "text": "Delisted sales",
            "font": {"family": "Arial", "size": 14},
            "x": 0.5,
        },
        hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    )

    fig2.update_layout(
        title={
            "text": "Transferable Sales",
            "font": {"family": "Arial", "size": 14},
            "x": 0.5,
        },
        hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    )

    fig3.update_layout(
        title={
            "text": "Total Impact",
            "font": {"family": "Arial", "size": 14},
            "x": 0.25,
        },
        hoverlabel=dict(bgcolor="white", font=dict(color="black")),
    )

    fig1.update_traces(hovertemplate="Sales: $%{y:,.2f}M<br>" "<extra></extra>")

    fig2.update_traces(hovertemplate="Sales: $%{y:,.2f}M<br>" "<extra></extra>")

    fig3.update_traces(hovertemplate="Sales: $%{y:,.2f}M<br>" "<extra></extra>")

    # Set the width and legend of the figures
    fig1.update_layout(width=220, showlegend=False)
    fig2.update_layout(width=220, showlegend=False)
    fig3.update_layout(
        width=220, legend={"title": "", "x": 2.5, "bgcolor": "rgba(0,0,0,0)"}
    )

    fig1.update_yaxes(tickprefix="$", ticksuffix="M")
    fig2.update_yaxes(tickprefix="$", ticksuffix="M")
    fig3.update_yaxes(tickprefix="$", ticksuffix="M")

    fig1.update_layout(xaxis={"showticklabels": False})
    fig2.update_layout(xaxis={"showticklabels": False})
    fig3.update_layout(xaxis={"showticklabels": False})

    # Remove the x-axis and y-axis labels from the figures
    fig1.update_xaxes(title_text="")
    fig1.update_yaxes(title_text="")
    fig2.update_xaxes(title_text="")
    fig2.update_yaxes(title_text="")
    fig3.update_xaxes(title_text="")
    fig3.update_yaxes(title_text="")

    # Set the background color of the figures to white
    fig1.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    fig2.update_layout(plot_bgcolor="white", paper_bgcolor="white")
    fig3.update_layout(plot_bgcolor="white", paper_bgcolor="white")

    return html.Div(
        [
            html.H3(
                scenario_name,
                style={
                    "border-left": "4px solid rgb(204,0,0)",
                    "padding-left": "10px",
                },
            ),
            html.Div(
                [
                    dcc.Graph(figure=fig1),
                    dcc.Graph(figure=fig2),
                    dcc.Graph(figure=fig3),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "margin-top": "10px",
                    "padding": "10px 15px",
                    "border-radius": "8px",
                },
            ),
        ],
        style={
            "font-family": "Arial",
            "display": "flex",
            "flex-direction": "column",
            "margin": "1.5rem 2rem",
            "background": "whitesmoke",
            "border-radius": "8px",
            "padding": "1rem",
        },
    )


if __name__ == "__main__":
    app.run_server(debug=True)
