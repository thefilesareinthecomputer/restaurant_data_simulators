import os
import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc

# initialize dash app with bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# load parquet file into pandas dataframe
parquet_file_path = os.path.join(os.path.dirname(__file__), 'data', 'sales_data.parquet')
df = pd.read_parquet(parquet_file_path)

# make sure dates are datetime ojbects
df['date'] = pd.to_datetime(df['date'])

# pre-compute data for performance
total_net_sales = df['net_sales'].sum()
net_sales_by_category = df.groupby('category')['net_sales'].sum().reset_index()
net_sales_by_location = df.groupby('location')['net_sales'].sum().reset_index()
top_25_menu_items = df.groupby('menu_item')['net_sales'].sum().reset_index().sort_values(by='net_sales', ascending=False).head(25)

# define app layout using dash bootstrap rows / columns / components
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Restaurant Sales Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Region Slicer"),
            dcc.Dropdown(
                id='region-slicer',
                options=[{'label': region, 'value': region} for region in df['region'].unique()],
                placeholder="Select a Region",
            ),
        ], width=3),

        dbc.Col([
            html.H4("Location Slicer"),
            dcc.Dropdown(
                id='location-slicer',
                options=[{'label': location, 'value': location} for location in df['location'].unique()],
                placeholder="Select a Location",
                multi=True
            ),
        ], width=3),

        dbc.Col([
            html.H4("Date Range Slicer"),
            dcc.DatePickerRange(
                id='date-range-slicer',
                min_date_allowed=df['date'].min(),
                max_date_allowed=df['date'].max(),
                start_date=df['date'].min(),
                end_date=df['date'].max()
            ),
        ], width=6),
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Menu Category Slicer"),
            dcc.Dropdown(
                id='category-slicer',
                options=[{'label': category, 'value': category} for category in df['category'].unique()],
                placeholder="Select a Menu Category",
            ),
        ], width=4),

        dbc.Col([
            html.H4("Menu Item Slicer"),
            dcc.Dropdown(
                id='menu-item-slicer',
                options=[{'label': item, 'value': item} for item in df['menu_item'].unique()],
                placeholder="Select a Menu Item",
                multi=True
            ),
        ], width=4),
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(
                id='total-net-sales-display', 
                className='card card-body bg-light mb-3',
                style={'fontSize': '32px', 'fontWeight': 'bold', 'textAlign': 'center'}
            ),
        ], width=12),
    ]),

    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id='sales-by-region-bar')), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id='sales-by-location-bar')), width=6),
    ]),

    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id='sales-by-category-bar')), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id='net-sales-by-item-bar-top-25')), width=6),
    ]),
])

# callbacks and functionality for responsive ui

# update total net sales single metric based on slicers
@app.callback(
    Output('total-net-sales-display', 'children'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date'),
     Input('category-slicer', 'value'),
     Input('menu-item-slicer', 'value')]
)
def update_total_net_sales(selected_region, selected_location, start_date, end_date, selected_category, selected_menu_item):
    filtered_df = df.copy()

    # ensure default values on initial load
    if not start_date or not end_date:
        start_date, end_date = df['date'].min(), df['date'].max()

    # apply filters
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]
    
    if selected_category:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    if selected_menu_item:
        filtered_df = filtered_df[filtered_df['menu_item'].isin(selected_menu_item)]

    # make sure not empty
    if filtered_df.empty:
        return "No data available for the selected filters."

    # make metric
    total_sales = filtered_df['net_sales'].sum()
    return f"Total Net Sales: ${total_sales:,.2f}"

# update total net sales by category bar chart based on slicers
@app.callback(
    Output('sales-by-category-bar', 'figure'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date'),
     Input('category-slicer', 'value'),
     Input('menu-item-slicer', 'value')]
)
def update_sales_by_category(selected_region, selected_location, start_date, end_date, selected_category, selected_menu_item):
    filtered_df = df.copy()

    # ensure default values on initial load
    if not start_date or not end_date:
        start_date, end_date = df['date'].min(), df['date'].max()

    # apply filters
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]
    
    if selected_category:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    if selected_menu_item:
        filtered_df = filtered_df[filtered_df['menu_item'].isin(selected_menu_item)]

    # make sure not empty
    if filtered_df.empty:
        return px.bar(title="No Data Available")

    # group by category and sum net sales
    sales_by_category = filtered_df.groupby('category')['net_sales'].sum().reset_index()

    # make chart
    fig = px.bar(
        sales_by_category,
        x='category',
        y='net_sales',
        title='Total Net Sales by Category'
    )
    return fig

# update total net sales per region bar chart based on slicers
@app.callback(
    Output('sales-by-region-bar', 'figure'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date'),
     Input('menu-item-slicer', 'value')]
)
def update_sales_by_region(selected_region, selected_location, start_date, end_date, selected_menu_item):
    filtered_df = df.copy()

    # ensure default values on initial load
    if not start_date or not end_date:
        start_date, end_date = df['date'].min(), df['date'].max()

    # apply filters
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]

    if selected_menu_item:
        filtered_df = filtered_df[filtered_df['menu_item'].isin(selected_menu_item)]

    # make sure not empty
    if filtered_df.empty:
        return px.bar(title="No Data Available")
    
    # group by region and sum net sales
    sales_by_region = filtered_df.groupby('region')['net_sales'].sum().reset_index()

    # create the chart
    fig = px.bar(
        sales_by_region,
        x='region',
        y='net_sales',
        title='Total Net Sales by Region',
        labels={'net_sales': 'Net Sales (USD)', 'region': 'Region'},
        text='net_sales'
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    return fig

# update top 25 menu items bar chart based on slicers
@app.callback(
    Output('net-sales-by-item-bar-top-25', 'figure'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date')]
)
def update_top_25_menu_items(selected_region, selected_location, start_date, end_date):
    filtered_df = df.copy()

    # ensure default values on initial load
    if not start_date or not end_date:
        start_date, end_date = df['date'].min(), df['date'].max()

    # apply filters
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]

    if filtered_df.empty:
        return px.bar(title="No Data Available")
    
    # group by menu item and sum net sales
    top_25_items = filtered_df.groupby('menu_item')['net_sales'].sum().reset_index().sort_values(by='net_sales', ascending=False).head(25)

    # make the bar chart
    fig = px.bar(
        top_25_items,
        x='menu_item',
        y='net_sales',
        title='Top 25 Menu Items by Total Net Sales',
        labels={'net_sales': 'Net Sales (USD)', 'menu_item': 'Menu Item'},
        text='net_sales'
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    return fig

# update total net sales by location bar chart based on slicers
@app.callback(
    Output('sales-by-location-bar', 'figure'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date'),
     Input('menu-item-slicer', 'value')]
)
def update_sales_by_location(selected_region, selected_location, start_date, end_date, selected_menu_item):
    filtered_df = df.copy()

    # ensure default values on initial load
    if not start_date or not end_date:
        start_date, end_date = df['date'].min(), df['date'].max()

    # apply filters
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]

    if selected_menu_item:
        filtered_df = filtered_df[filtered_df['menu_item'].isin(selected_menu_item)]

    # make sure not empty
    if filtered_df.empty:
        return px.bar(title="No Data Available")

    # group by location and sum net sales
    sales_by_location = filtered_df.groupby('location')['net_sales'].sum().reset_index()

    # make the bar chart
    fig = px.bar(
        sales_by_location,
        x='location',
        y='net_sales',
        title='Total Net Sales by Location',
        labels={'net_sales': 'Net Sales (USD)', 'location': 'Location'},
        text='net_sales'
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    return fig

# run app
if __name__ == '__main__':
    # app.run_server(host='0.0.0.0', port=8050, debug=True)
    # app.run_server(debug=True, host="0.0.0.0", port=8050)
    # dynamic port binding for render with default 8050 if not specified
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host='0.0.0.0', port=port)
