# import the necessary libraries/modules
import dash
from dash import dash_table
from dash import dcc, html
import base64
import pyodbc
import pandas as pd
import numpy as np
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


# consider the Sales_Exclusion column having row values = 0 (to avoid duplicates)
df = df[df['Sales_Exclusion'] == 0]

# make the internal sales and TNP in terms of millions and round off two one decimal place
df['Internal_Sales'] = df['Internal_Sales']/pow(10,6)
df['TNP'] = df['TNP']/pow(10,6)

# compute TNP percentage: TNP % = TNP / Sales
df['TNP %'] = np.where(df['Internal_Sales'] == 0, 0, df['TNP'] / df['Internal_Sales'])

# convert the Internal_Sales values to string after rounding off to one decimal place
df['Internal_Sales'] = df['Internal_Sales'].round(1).astype(str)

# round off to one decimal place
df['TNP'] = df['TNP'].round(1)

# convert to percentage and round off to one decimal place
df['TNP %'] = df['TNP %']*100
df['TNP %'] = df['TNP %'].round(1)

# append '$' and 'M' (Million) to the Sales and TNP values
df['Internal_Sales'] = df['Internal_Sales'].apply(lambda x: "$"+str(x)+"M")
df['TNP'] = df['TNP'].apply(lambda x: "$"+str(x)+"M")

# append '%' to the TNP % values
df['TNP %'] = df['TNP %'].apply(lambda x: str(x)+"%")

# rename the columns
df = df.rename(columns = {'Level_1_Name':'Category group',
                          'Level_2_Name':'Category',
                          'Level_3_Name':'Sub-category',
                          'Brand_Name':'Brand name',
                          'SKU_Name':'SKU name',
                          'Internal_Sales':'Sales',
                          'Group_Supplier_Name':'Supplier'})

# concatenation of Brand name and SKU name
df['Item'] = df['Brand name'].astype(str) + ' - ' + df['SKU name'].astype(str)

# access the required columns
df = df[["Category group",
         "Category",
         "Sub-category",
         "Supplier",
         "Item",
         "Internal/External",
         "Brand name",
         "Sales",
         "TNP",
         "TNP %"]]

# create Dash web application
app = dash.Dash()

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
        className='gray-pill'
)

category_dropdown = dcc.Dropdown(
    id='category-dropdown',
    options=df['Category'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'],
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        className='gray-pill'
)

sub_category_dropdown = dcc.Dropdown(
    id='sub-category-dropdown',
    options=df['Sub-category'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'], 
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        className='gray-pill'
)

Supplier_dropdown = dcc.Dropdown(
    id='Supplier-dropdown',
    options=df['Supplier'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'], 
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        className='gray-pill'
)

brand_dropdown = dcc.Dropdown(
    id='brand-dropdown',
    options=df['Brand name'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'], 
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        className='gray-pill'
)

item_dropdown = dcc.Dropdown(
    id='item-dropdown',
    options=df['Item'].unique(),
    multi=True,
    style={
        'backgroundColor': colors['background'],
        'color': colors['text'],
        'margin': '10px 0px 0px 0px'},
        className='gray-pill'
)


# create app layout
app.layout = html.Div([
    
    html.Div([

    # Heading
    html.H1('Category Plan',
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
        title='Note:\n1) All figures are based on data for Financial Year 2021'
    )

]),
    

    html.Div([
    # Sub-heading
    html.H4('What will be the final assortment for each category?',
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
        html.Span("Assortment planning  ❯", style={'color': 'rgb(170, 170, 170)'}),
        html.Span("  Planning review", style={'color': 'rgb(51, 51, 51)'})
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
        category_group_dropdown
    ], style={
        'width': '15%', 
        'display': 'inline-block', 
        'margin-left': '24px', 
        'margin-top': '25px', 
        'margin-bottom': '21px', 
        'border-right': '1px solid lightgray', 
        'padding': '10px',
        'fontSize': 15,
        'font-family': 'Arial'}),
    
    html.Div([
        html.Label('Category'),
        category_dropdown
    ], style={
        'width': '15%', 
        'display': 'inline-block', 
        'border-right': '1px solid lightgray', 
        'padding': '10px',
        'fontSize': 15,
        'font-family': 'Arial'}),

    html.Div([
        html.Label('Sub-category'),
        sub_category_dropdown
    ], style={
        'width': '15%', 
        'display': 'inline-block', 
        'border-right': '1px solid lightgray',
        'padding': '10px',
        'fontSize': 15,
        'font-family': 'Arial'}),

    html.Div([
        html.Label('Supplier'),
        Supplier_dropdown
    ], style={
        'width': '15%',
        'display': 'inline-block',
        'border-right': '1px solid lightgray',
        'padding': '10px',
        'fontSize': 15,
        'font-family': 'Arial'}),

    html.Div([
        html.Label('Brand'),
        brand_dropdown
    ], style={
        'width': '15%',
        'display': 'inline-block',
        'border-right': '1px solid lightgray',
        'padding': '10px',
        'fontSize': 15,
        'font-family': 'Arial'}),

    html.Div([
        html.Label('Item'),
        item_dropdown
    ], style={
        'width': '15%',
        'display': 'inline-block',
        'margin-left': '10px',
        'fontSize': 15,
        'font-family': 'Arial'}),
    ]),

    
    # Spreadsheet
    html.Div([
    dash_table.DataTable(
        id='spreadsheet',

        columns=[{"name": 'Category group', "id": 'Category group'},
                 {"name": 'Category', "id": 'Category'},
                 {"name": 'Sub-category', "id": 'Sub-category'},
                 {"name": 'Item', "id": 'Item'},
                 {"name": 'Internal/External', "id": 'Internal/External'},
                 {"name": 'Sales', "id": 'Sales'},
                 {"name": 'TNP', "id": 'TNP'},
                 {"name": 'TNP %', "id": 'TNP %'}],

        data=df.to_dict("records"),

        style_cell={
            'width': '100px',
            'textAlign': 'left',
            'backgroundColor': 'lightgray',
            'font-family': 'Arial',
            'font-size': '0.88em'},

        # adjusts the width of column bar
        style_data_conditional=[
                                {'if': {'column_id': 'Category group'},
                                    'width': '13%',
                                    'textAlign': 'left',
                                    'backgroundColor':'rgb(255,255,255)',
                                    'border':'thin lightgrey solid'},

                                {'if': {'column_id': 'Category'},
                                    'width': '14%', 
                                    'textAlign': 'left',
                                    'backgroundColor':'rgb(255,255,255)',
                                    'border':'thin lightgrey solid'},

                                { 'if': {'column_id': 'Sub-category'},
                                    'width': '13%', 
                                    'textAlign': 'left',
                                    'backgroundColor':'rgb(255,255,255)',
                                    'border':'thin lightgrey solid'},

                                {'if': {'column_id': 'Supplier'},
                                    'width': '16.66%',
                                    'textAlign': 'right'},

                                {'if': {'column_id': 'Internal/External'},
                                    'width': '8%',
                                    'textAlign': 'left',
                                    'backgroundColor':'rgb(255,255,255)',
                                    'border':'thin lightgrey solid'},

                                {'if': {'column_id': 'Item'},
                                    'width':'12%',
                                    'backgroundColor':'rgb(255,255,255)',
                                    'border':'thin lightgrey solid'},

                                {'if': {'column_id': 'Sales'},
                                    'width': '10%',
                                    'textAlign': 'left',
                                    'backgroundColor':'rgb(176,166,161)',
                                    'border':'thin lightgrey solid'},

                                {'if': {'column_id': 'TNP'},
                                    'width': '8%',
                                    'textAlign': 'left',
                                    'backgroundColor':'rgb(176,166,161)',
                                    'border':'thin lightgrey solid'},

                                {'if': {'column_id': 'TNP %'},
                                    'width': '6%',
                                    'textAlign': 'left', 
                                    'backgroundColor':'rgb(176,166,161)',
                                    'border':'thin lightgrey solid'}],

        style_cell_conditional=[{'if': {'column_id': 'Category group'}},
                                {'if': {'column_id': 'Category'},},
                                {'if': {'column_id': 'Sub-category'},},
                                {'if': {'column_id': 'Item'},},
                                {'if': {'column_id': 'Internal/External'},},
                                {'if': {'column_id': 'Sales'},'textFormat': '$0,0.00'},
                                {'if': {'column_id': 'TNP'},},
                                {'if': {'column_id': 'TNP %'},}
                                ],
        
        style_header={
            'backgroundColor': 'rgb(255, 255, 255)',
            'fontWeight': 'bold',
            'color': 'black',
            'fontSize': 15,
            'font-family': 'Arial',
            '.multi-select-dropdown':{'background-color': 'black','color': 'white'}
        },
        style_table={
            'overflowX': 'scroll',
            'overflowY': 'scroll',
            'fontSize': 15.4,
            'padding-left': '34px',
            'height': '67vh',
            'width': '189.6vh',
            'font-family': 'Arial',
            'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40}
           }
        )
    ])

])

# Create callback to update spreadsheet data based on dropdown value
@app.callback(
    Output('spreadsheet', 'data'),
    Input('category-group-dropdown', 'value'),
    Input('category-dropdown', 'value'),
    Input('sub-category-dropdown', 'value'),
    Input('Supplier-dropdown', 'value'),
    Input('brand-dropdown', 'value'),
    Input('item-dropdown', 'value'),
    #Input('Supplier-dropdown', 'value'),
)

def update_table(category_group,category,sub_category,Supplier,brand,item):
    dff = df
    if category_group:
        dff = dff[dff['Category group'].isin(category_group)]
    
    if category:
        dff = dff[dff['Category'].isin(category)]

    if sub_category:
        dff = dff[dff['Sub-category'].isin(sub_category)]

    if Supplier:
        dff = dff[dff['Supplier'].isin(Supplier)]
    
    if brand:
        dff = dff[dff['Brand name'].isin(brand)]

    if item:
        dff = dff[dff['Item'].isin(item)]

    return dff.to_dict('records')

    
# run web application
if __name__ == '__main__':
    app.run_server(debug=True)