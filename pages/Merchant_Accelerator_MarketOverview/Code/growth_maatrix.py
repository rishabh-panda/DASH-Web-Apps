
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


# read spreadsheet from the database using pandas
df = pd.read_csv('Assets/Consumption_market (product_testing)_Consumption_Market.csv', low_memory=False, dtype={'Financial Year': 'str'})


# rename the columns
df = df.rename(columns = {'Brand Name':'Brand',
                          'Group Supplier Name':'Supplier name'})

# access the required columns
df = df[["Category group",
         "Category",
         "Brand",
         "Supplier name",
         "Financial Year",
         "Sales",
         "Market Type",
         "Retailer"]]

x_value = 6

dff = df

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


    
#RetailCo_data_filtered = RetailCo_data_filtered.groupby(['Supplier name']).agg({'Sales' : 'sum'})
#RetailCo_data_filtered = RetailCo_data_filtered.reset_index()
#RetailCo_data_filtered_1 = RetailCo_data_filtered.groupby(['Supplier name'])['Sales'].sum().reset_index().sort_values(['Sales'], ascending=False)

## Extract unique suppliers from the 'Supplier name' column
#included_suppliers = RetailCo_data_filtered_1['Supplier name'].unique().tolist()
#included_suppliers = included_suppliers[0:x_value]

#if x_value == 0:
#    RetailCo_data_filtered = RetailCo_data_filtered
#else:
#    RetailCo_data_filtered = RetailCo_data_filtered[RetailCo_data_filtered['Supplier name'].isin(included_suppliers)]


#ROM_data_filtered = ROM_data_filtered.groupby(['Supplier name']).agg({'Sales' : 'sum'})
#ROM_data_filtered = ROM_data_filtered.reset_index()
#ROM_data_filtered_1 = ROM_data_filtered.groupby(['Supplier name'])['Sales'].sum().reset_index().sort_values(['Sales'], ascending=False)

## Extract unique suppliers from the 'Supplier name' column
#included_suppliers = ROM_data_filtered_1['Supplier name'].unique().tolist()
#included_suppliers = included_suppliers[0:x_value]

#if x_value == 0:
#    ROM_data_filtered = ROM_data_filtered
#else:
#    ROM_data_filtered = ROM_data_filtered[ROM_data_filtered['Supplier name'].isin(included_suppliers)]



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
    title='<b>Growth matrix</b>',
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

fig.update_layout(height=450, width=800, showlegend=False)
fig.show()