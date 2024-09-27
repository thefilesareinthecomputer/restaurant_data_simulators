import os
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Load the Parquet file into a pandas DataFrame
parquet_file_path = os.path.join(os.path.dirname(__file__), 'data', 'sales_data.parquet')
df = pd.read_parquet(parquet_file_path)

# Create a 'week' column for aggregation by week
df['week'] = pd.to_datetime(df['date']).dt.isocalendar().week

# Precompute some data for faster rendering
total_net_sales = df['net_sales'].sum()
net_sales_by_category = df.groupby('category')['net_sales'].sum().reset_index()
net_sales_by_location = df.groupby('location')['net_sales'].sum().reset_index()
top_25_menu_items = df.groupby('menu_item')['net_sales'].sum().reset_index().sort_values(by='net_sales', ascending=False).head(25)

# Define app layout
app.layout = html.Div([
    html.H1("Restaurant Sales Dashboard"),

    # Region slicer
    dcc.Dropdown(
        id='region-slicer',
        options=[{'label': region, 'value': region} for region in df['region'].unique()],
        placeholder="Select a Region",
    ),

    # Location slicer
    dcc.Dropdown(
        id='location-slicer',
        options=[{'label': location, 'value': location} for location in df['location'].unique()],
        placeholder="Select a Location",
        multi=True
    ),

    # Date range slicer
    dcc.DatePickerRange(
        id='date-range-slicer',
        min_date_allowed=df['date'].min(),
        max_date_allowed=df['date'].max(),
        start_date=df['date'].min(),
        end_date=df['date'].max()
    ),

    # Menu Category slicer
    dcc.Dropdown(
        id='category-slicer',
        options=[{'label': category, 'value': category} for category in df['category'].unique()],
        placeholder="Select a Menu Category",
    ),

    # Menu Item slicer
    dcc.Dropdown(
        id='menu-item-slicer',
        options=[{'label': item, 'value': item} for item in df['menu_item'].unique()],
        placeholder="Select a Menu Item",
        multi=True
    ),

    # Display total net sales (Single Value)
    html.Div(id='total-net-sales-display'),

    # Total Net Sales by Category (Bar Chart)
    dcc.Graph(id='sales-by-category-bar'),

    # Total Net Sales by Location (Bar Chart)
    dcc.Graph(id='sales-by-location-bar'),

    # Top 25 Menu Items org-wide by Total Net Sales (Data Table)
    html.Div(id='top-25-menu-items-table'),

    # Top 5 Menu Items per Region by Total Net Sales (Bar Chart)
    dcc.Graph(id='top-5-menu-items-region-bar'),

    # Top 5 Sales Weeks per Location (Heatmap)
    dcc.Graph(id='top-5-weeks-location-heatmap'),

    # Total Net Sales by Category (Bar Chart)
    dcc.Graph(id='net-sales-by-category-bar')
])

# CALLBACKS
# Callback to update Total Net Sales based on slicers
@app.callback(
    Output('total-net-sales-display', 'children'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date')]
)
def update_total_net_sales(selected_region, selected_location, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]

    total_sales = filtered_df['net_sales'].sum()
    return f"Total Net Sales: ${total_sales:,.2f}"

# Callback to update Total Net Sales by Category (Bar Chart)
@app.callback(
    Output('sales-by-category-bar', 'figure'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date')]
)
def update_sales_by_category(selected_region, selected_location, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]

    sales_by_category = filtered_df.groupby('category')['net_sales'].sum().reset_index()

    fig = px.bar(
        sales_by_category,
        x='category',
        y='net_sales',
        title='Total Net Sales by Category'
    )
    return fig

# Callback for Top 5 Menu Items per Region by Total Net Sales
@app.callback(
    Output('top-5-menu-items-region-bar', 'figure'),
    [Input('region-slicer', 'value'),
     Input('location-slicer', 'value'),
     Input('date-range-slicer', 'start_date'),
     Input('date-range-slicer', 'end_date')]
)
def update_top_5_menu_items(selected_region, selected_location, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if selected_region:
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_location:
        filtered_df = filtered_df[filtered_df['location'].isin(selected_location)]

    top_5_items = filtered_df.groupby('menu_item')['net_sales'].sum().reset_index().sort_values(by='net_sales', ascending=False).head(5)

    fig = px.bar(
        top_5_items,
        x='menu_item',
        y='net_sales',
        title='Top 5 Menu Items per Region'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
