# import the necessary libraries/modules
import dash
from dash import dcc, html
import json
import base64
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pandas as pd
import pyodbc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Output, Input

cnxn_str=("DRIVER={ODBC Driver 17 for SQL Server};",
          "SERVER=aag-a7rw-sql-server.database.windows.net;",
          "DATABASE=product_testing;",
          "Trusted_Connection=yes;",
          "UID=;",
          "PWD=;")

cnxn_str = ";".join(cnxn_str)

# Establish connection with SQL server
cnxn = pyodbc.connect(cnxn_str)

#Read data for relaying to the code
df = pd.read_sql("SELECT * FROM consumption.abs_cereals_sku_action", cnxn)



# rename the columns
df = df.rename(columns = {'Brand_Name':'Brand',
                          'Group_Supplier_Name':'Supplier name',
                          'Level_1_Name':'Category group',
                          'Level_2_Name':'Category',
                          'Overall_Sales':'Sales',
                          'Market_Type':'Market Type',})

# access the required columns
df = df[["Category group",
         "Category",
         "Brand",
         "Supplier name",
         "Sales",
         "Market Type"]]


# create Dash web application
app = dash.Dash()

dash.register_page(__name__)

# save the Merchant Accelerator logo in a variable
ma_logo_png = r'./Assets/MA logo red.png'
ma_logo_base64 = base64.b64encode(open(ma_logo_png, 'rb').read()).decode('ascii')

# save the Home logo in a variable
home_logo_png = r'./Assets/home.png'
home_logo_base64 = base64.b64encode(open(home_logo_png, 'rb').read()).decode('ascii')

# save the Info logo in a variable
info_logo_png = r'./Assets/info.png'
info_logo_base64 = base64.b64encode(open(info_logo_png, 'rb').read()).decode('ascii')

# define the color scheme
colors = {
    'background': 'white',
    'text': 'rgb(51,51,51)'
}

# create dropdown components
category_group_dropdown = dcc.Dropdown(
    id='category-group-dropdown',
    options=df['Category group'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'],
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        
)

category_dropdown = dcc.Dropdown(
    id='category-dropdown',
    options=df['Category'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'],
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        
)

brand_dropdown = dcc.Dropdown(
    id='brand-dropdown',
    options=df['Brand'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'], 
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        
)

# craete dropdown options
options = [{'label': x, 'value': x} for x in df['Supplier name'].unique() if not pd.isnull(x)]


supplier_name_dropdown = dcc.Dropdown(
    id='supplier-name-dropdown',
    options=options,
    multi=True,
    style={
        'backgroundColor': colors['background'], 
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        
)


# create app layout
app.layout = html.Div([
    
    html.Div([

    # Heading
    html.H1('Assortment optimization',
            style={
                'display':'inline-block',
                'color': 'rgb(204, 0, 0)',
                'height':'80px',
                'font-weight': 'bold',
                'margin-left': '35px',
                'margin-bottom': '-0.2px',
                'fontSize': 27,
                'font-family': 'Arial'}),
    

    # Merchant Accelerator Logo
    html.Img(
        src='data:image/png;base64,{}'.format(ma_logo_base64),
        style={'width': '350px', 'height': 'auto', 'margin-left': '1400px', 'margin-right': '200px', 'margin-top': '-70px', 'margin-bottom': '10px', 'float': 'right'}),

    # Home Logo
    html.Img(
        src='data:image/png;base64,{}'.format(home_logo_base64),
        style={'width': '30px', 'height': 'auto', 'margin-left': '1000px', 'margin-right': '130px', 'margin-top': '-72px', 'margin-bottom': '10px', 'float': 'right'}),

    # Info Logo
    html.Img(
        src='data:image/png;base64,{}'.format(info_logo_base64),
        style={'width': '34px', 'height': 'auto', 'margin-left': '100px', 'margin-right': '60px', 'margin-top': '-72px', 'margin-bottom': '10px', 'float': 'right'},
        title='Note:\n1) YoY is calculated for FY2020-21\n2) Fair share gap refers to the Sales RetailCo would gain/lose if the category has the same market share as the market growth matrix\n3) Dotted grey lines represent category average\n\n Source: Market data'
    )

]),
    

    html.Div([
    # Sub-heading
    html.H4('Which items could be removed from our assortment?',
            style={
                'display': 'flex', 
                'justify-content': 'space-between',
                'margin-left': '35px',
                'margin-top': '-50px',
                'font-weight': 'normal',
                'fontSize': 18,
                'color': colors['text'],
                'font-family': 'Arial'}),
    ]),


    # Gray bar denoting: 'Assortment planning ❯ Planning review'
    html.Div([
        html.Span("Assortment planning 〉", style={'color': 'rgb(170, 170, 170)'}),
        html.Span("  Assortment decisions", style={'color': 'rgb(51, 51, 51)'})
        ],
            style={
                'background-color': 'rgb(226,226,226)',
                'text-align': 'left',
                'height': '30px',
                'width' : '1808px',
                'margin-left': '35px', 
                'margin-right': '0px',
                'fontSize': 15,
                'font-family': 'Arial', 
                'padding-top': '10px', 
                'padding-bottom': '2px', 
                'padding-left': '10px',
                'white-space': 'nowrap'}),


    # Dropdowns
    html.Div([    
        html.Div([        
            html.Label('Category group'),        
            category_group_dropdown], 
                 style={
                    'width': '15%', 
                    'display': 'inline-block', 
                    'margin-left': '24px', 
                    'margin-top': '25px', 
                    'margin-bottom': '20px', 
                    'border-right': '1px solid lightgray', 
                    'padding': '10px',
                    'fontSize': 15,
                    'font-family': 'Arial'}),
    
    html.Div([        
        html.Label('Category'),        
              category_dropdown ],
             style={
                'width': '15%', 
                'display': 'inline-block', 
                'border-right': '1px solid lightgray', 
                'padding': '10px',
                'fontSize': 15,
                'font-family': 'Arial'}),

    html.Div([        
        html.Label('Brand'),        
        brand_dropdown], 
             style={
                'width': '15%',
                'display': 'inline-block',
                'border-right': '1px solid lightgray',
                'padding': '10px',
                'fontSize': 15,
                'font-family': 'Arial'}),

    html.Div([       
       html.Label('Supplier name'),        
       supplier_name_dropdown], 
             style={
                'width': '15%',
                'display': 'inline-block',
                'border-right': '1px solid lightgray',
                'padding': '10px',
                'fontSize': 15,
                'font-family': 'Arial'}),

    html.Div([            
        html.Div('Top x suppliers', 
                 style={'padding': '10px', 
                        'margin-top': '24px',
                        'display': 'inline-block', 
                        'vertical-align': 'top'}),                    
        dcc.Input(                            
            id='my-input',                            
            type='number',                            
            value='0',                            
            min='0',                            
            style={                                    
                'width': '85%',
                'height': '14px',
                'border': '1px solid lightgray',
                'border-radius': '4px',
                'display': 'inline-block',                                    
                'padding': '10px',                                    
                'fontSize': 15,                                    
                'font-family': 'Arial',
                'margin': '-1px 0 0 10px'
                })        
        ], 
             style={'display': 'inline-block', 
                    'vertical-align': 'top', 
                    'width': '15%'})
    ], 
    style={'display': 'inline-block', 
           'width': '100%'}),
    
    html.Div([
        dcc.Graph(id='my-graph1', style={'margin-right': '40px'}),
        dcc.Graph(id='my-graph2',
                  style={'margin-left': '57px'})
    ],
        style={'display': 'flex',
               'flex-direction':'row',
               'margin-left': '37px',
               'margin-top': '-27px',
               'margin-top': '20px',}),

    html.Div([
        dcc.Graph(id='my-graph3', style={'margin-right': '40px'}),
        dcc.Graph(id='my-graph4',
                  style={'margin-left': '57px'}),
    ],
        style={'display': 'flex',
               'flex-direction':'row',
               'margin-left': '35px',
               'margin-top': '-27px'})

])

# defining height and width of the stacked bar charts
height = 430
width = 700

# 1. Create callback to update Market Sales data based on input values
@app.callback(
    Output('my-graph1', 'figure'),
    Input('category-group-dropdown', 'value'),
    Input('category-dropdown', 'value'),
    Input('brand-dropdown', 'value'),
    Input('supplier-name-dropdown', 'value'),
    Input('my-input', 'value')
)
def update_graph(category_group, category, brand, supplier_name, value):
    dff = df

    # taking dropdowns into account
    if category_group:
        dff = dff[dff['Category group'].isin(category_group)]

    if category:
        dff = dff[dff['Category'].isin(category)]

    if brand:
        dff = dff[dff['Brand'].isin(brand)]

    if supplier_name:
        dff = dff[dff['Supplier name'].isin(supplier_name)]

    dff = dff.reset_index(drop=True)


    # Filter the data where 'Retailer' is 'Market'
    market_data = dff[dff['Retailer'] == 'Market']

    # group the data by 'Supplier name' and 'Financial Year' for Market
    grouped_market = market_data.groupby(['Supplier name', 'Financial Year'])

    # calculate the total sales for each supplier and year for Market
    sales_market = grouped_market['Sales'].sum()

    # get the sales for 2020 and 2021 for each supplier for Market
    sales_2020_market = sales_market.loc[:, '2020']

    sales_2021_market = sales_market.loc[:, '2021']

    yoy_growth_market = ((sales_2021_market - sales_2020_market) / sales_2020_market) * 100


    dff['Sales'] = pd.to_numeric(dff['Sales'])
    dff['Sales'] = dff['Sales'] / 1000000  # 10^6

    if value:
        sorted_df = dff.groupby(['Supplier name', 'Financial Year'])['Sales'].sum().reset_index().sort_values(['Supplier name', 'Financial Year'], ascending=True)
        supplier_names = sorted_df['Supplier name'].unique().tolist()

        data = []
        yoy_sales_data = [] # Added for displaying yoy_growth_Market values

        for supplier in supplier_names:
            trace = go.Bar(
                x=sorted_df[sorted_df['Supplier name'] == supplier]['Financial Year'],
                y=sorted_df[sorted_df['Supplier name'] == supplier]['Sales'],
                name=supplier
            )
            data.append(trace)

            yoy_growth_market = ((sales_2021_market - sales_2020_market) / sales_2020_market) * 100
            yoy_growth_market = yoy_growth_market.values[0]

            yoy_sales_trace = go.Scatter(
                x=[sorted_df[sorted_df['Supplier name'] == supplier]['Financial Year'].iloc[-1]],
                y=[yoy_growth_market],
                mode="none",
                text=["{}%".format(format(yoy_growth_market, '.2f'))],
                textposition="middle right",
                showlegend=False,
                yaxis='y2'
            )

            yoy_sales_data.append(yoy_sales_trace)

        total_sales = dff.groupby('Financial Year')['Sales'].sum().values.tolist()

        annotations = []
        for i in range(len(total_sales)):
            annotations.append(
                dict(
                    x=i,
                    y=max(total_sales) * 1.05,
                    text='<b>${:,.0f}'.format(total_sales[i]) + 'M</b>',
                    showarrow=False,
                    font=dict(family='Arial', size=12)
                )
            )
        
        
        layout = go.Layout(
            barmode='stack',
            title={
                'text': "Market Sales",
                'font': {
                    'family': 'Arial Bold',
                    'size': 20
                }
            },

            yaxis=dict(title='Market sales', tickprefix='$', ticksuffix='M', tickformat=',.0f'),
            yaxis2=dict(
                title='YoY',
                overlaying='y',
                side='right',
                tickprefix='', 
                ticksuffix='%',
                tickformat='.2f',
                showgrid=False
            ),
            plot_bgcolor='white',
            annotations=annotations
        )

        fig = go.Figure(data=data+yoy_sales_data, layout=layout) # Adding yoy_sales_data to the figure
        fig.update_layout(height=height, width=width, showlegend=False)

        return fig

    else:
        return {}




# 2. Create callback to update RetailCo's Sales data based on input values
@app.callback(
    Output('my-graph2', 'figure'),
    Input('category-group-dropdown', 'value'),
    Input('category-dropdown', 'value'),
    Input('brand-dropdown', 'value'),
    Input('supplier-name-dropdown', 'value'),
    Input('my-input', 'value')
)

def update_graph(category_group, category, brand, supplier_name, value):
    dff = df

    # taking dropdowns into account
    if category_group:
        dff = dff[dff['Category group'].isin(category_group)]

    if category:
        dff = dff[dff['Category'].isin(category)]

    if brand:
        dff = dff[dff['Brand'].isin(brand)]

    if supplier_name:
        dff = dff[dff['Supplier name'].isin(supplier_name)]

    dff = dff.reset_index(drop=True)


    # Filter the data where 'Retailer' is 'RetailCo'
    RetailCo_data = dff[dff['Retailer'] == 'RetailCo']

    # group the data by 'Supplier name' and 'Financial Year' for Market
    grouped_RetailCo = RetailCo_data.groupby(['Supplier name', 'Financial Year'])

    # calculate the total sales for each supplier and year for Market
    sales_RetailCo = grouped_RetailCo['Sales'].sum()

    # get the sales for 2020 and 2021 for each supplier for Market
    sales_2020_RetailCo = sales_RetailCo.loc[:, '2020']

    sales_2021_RetailCo = sales_RetailCo.loc[:, '2021']

    yoy_growth_RetailCo = ((sales_2021_RetailCo - sales_2020_RetailCo) / sales_2020_RetailCo) * 100


    dff['Sales'] = pd.to_numeric(dff['Sales'])
    dff['Sales'] = dff['Sales'] / 1000000  # 10^6

    if value:
        sorted_df = dff.groupby(['Supplier name', 'Financial Year'])['Sales'].sum().reset_index().sort_values(['Supplier name', 'Financial Year'], ascending=True)
        supplier_names = sorted_df['Supplier name'].unique().tolist()

        data = []
        yoy_sales_data = [] # Added for displaying yoy_growth_Market values

        for supplier in supplier_names:
            trace = go.Bar(
                x=sorted_df[sorted_df['Supplier name'] == supplier]['Financial Year'],
                y=sorted_df[sorted_df['Supplier name'] == supplier]['Sales'],
                name=supplier
            )
            data.append(trace)

            yoy_growth_RetailCo = ((sales_2021_RetailCo - sales_2020_RetailCo) / sales_2020_RetailCo) * 100
            yoy_growth_RetailCo = yoy_growth_RetailCo.values[0]

            yoy_sales_trace = go.Scatter(
                x=[sorted_df[sorted_df['Supplier name'] == supplier]['Financial Year'].iloc[-1]],
                y=[yoy_growth_RetailCo],
                mode="none",
                text=["{}%".format(format(yoy_growth_RetailCo, '.2f'))],
                textposition="middle right",
                showlegend=False,
                yaxis='y2'
            )

            yoy_sales_data.append(yoy_sales_trace)

        total_sales = dff.groupby('Financial Year')['Sales'].sum().values.tolist()

        annotations = []
        for i in range(len(total_sales)):
            annotations.append(
                dict(
                    x=i,
                    y=max(total_sales) * 1.05,
                    text='<b>${:,.0f}'.format(total_sales[i]) + 'M</b>',
                    showarrow=False,
                    font=dict(family='Arial', size=12)
                )
            )
        
        
        layout = go.Layout(
            barmode='stack',
            title={
                'text': "RetailCo Sales",
                'font': {
                    'family': 'Arial Bold',
                    'size': 20
                }
            },

            yaxis=dict(title='RetailCo sales', tickprefix='$', ticksuffix='M', tickformat=',.0f'),
            yaxis2=dict(
                title='YoY',
                overlaying='y',
                side='right',
                tickprefix='', 
                ticksuffix='%',
                tickformat='.2f',
                showgrid=False
            ),
            plot_bgcolor='white',
            annotations=annotations
        )

        fig = go.Figure(data=data+yoy_sales_data, layout=layout) # Adding yoy_sales_data to the figure
        fig.update_layout(height=height, width=width, showlegend=False)

        return fig

    else:
        return {}



# 3. Create callback to update Fair share gap data based on input values
@app.callback(
    Output('my-graph3', 'figure'),
    Input('category-group-dropdown', 'value'),
    Input('category-dropdown', 'value'),
    Input('brand-dropdown', 'value'),
    Input('supplier-name-dropdown', 'value'),
    Input('my-input', 'value')
)

def update_graph(category_group, category, brand, supplier_name, value):
    dff = df

    overall_RetailCo_sales = dff.loc[(dff['Retailer'] == 'RetailCo') & (dff['Financial Year'] == '2021'), 'Sales'].sum()

    # Filter the data where 'Retailer' is 'RetailCo'
    retailco_data = dff[dff['Retailer'] == 'RetailCo']

    # Group the filtered data by unique 'Supplier name' and sum up the corresponding 'Sales' values
    sales_by_supplier_RetailCo = retailco_data.groupby('Supplier name')['Sales'].sum()

    # Divide each supplier's sales value by the overall_RetailCo_sales to get the share of wallet
    share_of_wallet_RetailCo = (sales_by_supplier_RetailCo / overall_RetailCo_sales).rename('Share of wallet RetailCo')

    share_of_wallet_RetailCo_perc = share_of_wallet_RetailCo*100

    # summing the 'Market Sales TY' values for 'Retailer' not equals to 'RetailCo'
    overall_ROM_sales = dff.loc[(dff['Retailer'] != 'RetailCo') & (dff['Financial Year'] == '2021'), 'Sales'].sum()

    # Filter the data where 'Retailer' is not 'RetailCo'
    ROM_data = dff[dff['Retailer'] != 'RetailCo']

    # Group the filtered data by unique 'Supplier name' and sum up the corresponding 'Sales' values
    sales_by_supplier_ROM = ROM_data.groupby('Supplier name')['Sales'].sum()

    # Divide each supplier's sales value by the overall_RetailCo_sales to get the share of wallet
    share_of_wallet_ROM = (sales_by_supplier_ROM / overall_ROM_sales).rename('Share of wallet ROM')

    share_of_wallet_ROM_perc = share_of_wallet_ROM*100

    fair_share_gap = share_of_wallet_RetailCo_perc - share_of_wallet_ROM_perc

    # bar chart values
    fair_share_sales = (sales_by_supplier_ROM - sales_by_supplier_RetailCo)*fair_share_gap



    # taking dropdowns into account
    if category_group:
        dff = dff[dff['Category group'].isin(category_group)]

    if category:
        dff = dff[dff['Category'].isin(category)]

    if brand:
        dff = dff[dff['Brand'].isin(brand)]

    if supplier_name:
        dff = dff[dff['Supplier name'].isin(supplier_name)]

    dff = dff.reset_index(drop=True)
   

    dff = dff.dropna(subset=['Supplier name'])

    # Extract unique suppliers from the 'Supplier name' column
    included_suppliers = dff['Supplier name'].unique()

    # Filter the fair_share_sales Series to include only the selected suppliers
    filtered_sales = fair_share_sales.loc[included_suppliers]

    # Divide the sales values by 1000 to display values in millions
    filtered_sales = filtered_sales / 1000

    # Set the bar color based on the sign of the y-values
    colors = ['rgb(89, 161, 79)' if val >= 0 else 'rgb(225, 87, 89)' for val in filtered_sales]


    # Create the bar chart using the filtered sales data
    fig = px.bar(
        x=filtered_sales.index, 
        y=filtered_sales.values,
        color = colors,
        labels={'x':' ', 'y':'Fair share sales'})

    # Add text annotations to the bars
    annotations = []
    for i, val in enumerate(filtered_sales.values):
        if val >= 0:
            annotations.append(dict(x=filtered_sales.index[i], 
                                    y=val,
                                    text=f"<b>${val/1000000:.1f}M</b>", 
                                    xanchor='center', 
                                    yanchor='bottom', 
                                    showarrow=False))
        else:
            annotations.append(dict(x=filtered_sales.index[i], 
                                    y=val, 
                                    text=f"<b>${abs(val)/1000000:.1f}M</b>", 
                                    xanchor='center', 
                                    yanchor='top', 
                                    showarrow=False))

    fig.update_layout(plot_bgcolor='white',
                     paper_bgcolor='white', 
                     title = 'Fair share gap',
                     showlegend=False, height=height, 
                     xaxis={'side': 'top'}, 
                     annotations=annotations)

    fig.update_xaxes(
    tickfont=dict(family='sans-serif', size=13, color='black'),
    tickmode='linear',
    tickangle=0,
    tickprefix='<span style="font-weight: bold;">',
    ticksuffix='</span>'
    )

    return fig


# 4. Create callback to update Growth matrix data based on input values
@app.callback(
    Output('my-graph4', 'figure'),
    Input('category-group-dropdown', 'value'),
    Input('category-dropdown', 'value'),
    Input('brand-dropdown', 'value'),
    Input('supplier-name-dropdown', 'value'),
    Input('my-input', 'value')
)

def update_graph(category_group, category, brand, supplier_name, value):
    dff = df

    # taking dropdowns into account
    if category_group:
        dff = dff[dff['Category group'].isin(category_group)]

    if category:
        dff = dff[dff['Category'].isin(category)]

    if brand:
        dff = dff[dff['Brand'].isin(brand)]

    if supplier_name:
        dff = dff[dff['Supplier name'].isin(supplier_name)]

    dff = dff.reset_index(drop=True)

    # Filter the data where 'Retailer' is 'RetailCo'
    RetailCo_data = dff[dff['Retailer'] == 'RetailCo']

    # Filter the data where 'Retailer' is not 'RetailCo'
    ROM_data = dff[dff['Retailer'] != 'RetailCo']

    # group the data by 'Supplier name' and 'Financial Year' for RetailCo and ROM
    grouped_RetailCo = RetailCo_data.groupby(['Supplier name', 'Financial Year'])
    grouped_ROM = ROM_data.groupby(['Supplier name', 'Financial Year'])

    # calculate the total sales for each supplier and year for RetailCo and ROM
    sales_retailCo = grouped_RetailCo['Sales'].sum()
    sales_ROM = grouped_ROM['Sales'].sum()

    # get the sales for 2020 and 2021 for each supplier for RetailCo and ROM
    sales_2020_RetailCo = sales_retailCo.loc[:, '2020']
    sales_2020_ROM = sales_ROM.loc[:, '2020']

    sales_2021_RetailCo = sales_retailCo.loc[:, '2021']
    sales_2021_ROM = sales_ROM.loc[:, '2021']

    # calculate the year-on-year sales growth percentage for each supplier for RetailCo and ROM
    yoy_growth_RetailCo = ((sales_2021_RetailCo-sales_2020_RetailCo) / sales_2020_RetailCo) * 100
    yoy_growth_ROM = ((sales_2021_ROM-sales_2020_ROM) / sales_2020_ROM) * 100


    height = 400
    width = 900

    # Filter out rows with NaN values in the 'Supplier name' column
    RetailCo_data_filtered = RetailCo_data[~RetailCo_data['Supplier name'].isna()]

    # Use boolean indexing to filter the RetailCo_data DataFrame
    RetailCo_data_filtered = RetailCo_data_filtered[
        RetailCo_data_filtered['Supplier name'].str.contains('Supplier')
        | RetailCo_data_filtered['Supplier name'].str.contains('Own Brand')]
    
    
    # Filter out rows with NaN values in the 'Supplier name' column
    ROM_data_filtered = RetailCo_data[~RetailCo_data['Supplier name'].isna()]

    # Use boolean indexing to filter the ROM_data DataFrame
    ROM_data_filtered = ROM_data_filtered[ROM_data_filtered['Supplier name'].str.contains('Supplier')
                                          | ROM_data_filtered['Supplier name'].str.contains('Own Brand')]

    # Calculate the year-on-year sales growth percentage for the filtered data
    yoy_growth_RetailCo = ((sales_2021_RetailCo[RetailCo_data_filtered['Supplier name'].dropna()] -
                            sales_2020_RetailCo[RetailCo_data_filtered['Supplier name'].dropna()]) /
                           sales_2020_RetailCo[RetailCo_data_filtered['Supplier name'].dropna()]) * 100

    yoy_growth_ROM = ((sales_2021_ROM[ROM_data_filtered['Supplier name'].dropna()] -
                       sales_2020_ROM[ROM_data_filtered['Supplier name'].dropna()]) /
                      sales_2020_ROM[ROM_data_filtered['Supplier name'].dropna()]) * 100

    # Create a trace for RetailCo
    trace1 = go.Scatter(
        x=yoy_growth_ROM,
        y=yoy_growth_RetailCo,
        mode='markers',
        marker=dict(
            size=sales_2021_RetailCo[RetailCo_data_filtered['Supplier name'].dropna()],
            sizemode='area',
            sizeref=2. * max(sales_2021_RetailCo[RetailCo_data_filtered['Supplier name'].dropna()]) / (40. ** 2),
            sizemin=4,
            #color=yoy_growth_ROM[suppliers],
            color='rgb(45,71,90)',
            colorscale='YlGnBu',
            opacity=0.5
        ),
        name='RetailCo'
    )

    # Create a trace for ROM
    trace2 = go.Scatter(
        x=yoy_growth_ROM,
        y=yoy_growth_RetailCo,
        mode='markers',
        marker=dict(
            size=sales_2021_ROM[ROM_data_filtered['Supplier name'].dropna()],
            sizemode='area',
            sizeref=2. * max(sales_2021_ROM[ROM_data_filtered['Supplier name'].dropna()]) / (40. ** 2),
            sizemin=4,
            #color=yoy_growth_ROM[suppliers],
            color='rgb(45,71,90)',
            colorscale='PiYG',
            opacity=0.5
        ),
        name='ROM'
    )

    data = [trace1, trace2]

    # Calculate the average values for both axes
    # Calculate the average values for both axes
    avg_x = yoy_growth_ROM.mean()
    avg_y = yoy_growth_RetailCo.mean()

    # Create a layout for the chart with adjusted axis ranges
    x_axis_range = [-1, 10]
    y_axis_range = [0, 20]
    y_axis_upper_bound = avg_y + 2  # Add 2 to the y-axis upper bound for the average value line
    layout = go.Layout(
        title='Growth matrix',
        xaxis=dict(title='ROM sales YoY', range=x_axis_range, dtick=1, ticksuffix='%'),
        yaxis=dict(title='RetailCo sales YoY', range=y_axis_range, dtick=5, ticksuffix='%'),
        plot_bgcolor='white'
    )

    # Add the traces for average value lines
    data.append(go.Scatter(x=[avg_x, avg_x], y=[y_axis_range[0], y_axis_range[1]],
                           mode='lines', name='Average ROM sales YoY', line=dict(dash='dot', color='lightgray')))
    data.append(go.Scatter(x=[x_axis_range[0], x_axis_range[1]], y=[avg_y, avg_y],
                           mode='lines', name='Average RetailCo sales YoY', line=dict(dash='dot', color='lightgray')))

    # Create the figure and show the chart
    fig = go.Figure(data=data, layout=layout)

    # Update the y-axis range in the layout to include the new upper bound for the average value line
    fig.update_layout(yaxis=dict(range=[y_axis_range[0], y_axis_upper_bound], dtick=5, ticksuffix='%'))

    fig.update_layout(height=height, width=width, showlegend=False)
    return fig


    
# run web application
if __name__ == '__main__':
    app.run_server(debug=True)