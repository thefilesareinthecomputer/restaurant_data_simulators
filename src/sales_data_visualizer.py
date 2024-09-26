import os
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()
PROJECT_DIRECTORY = os.getenv('PROJECT_DIRECTORY')

# Load the CSV file into a DataFrame
data_path = os.path.join(PROJECT_DIRECTORY, 'src', 'generated_data')
# create the data path if it doesn't exist
if not os.path.exists(data_path):
    os.makedirs(data_path)
file_name = f'{data_path}/sales_data_per_location_2024-09-26_16-50-15.csv'
df = pd.read_csv(file_name)

# Aggregate sales data by menu item (sum quantity_sold and net_sales)
product_sales = df.groupby('menu_item').agg(
    total_quantity_sold=('quantity_sold', 'sum'),
    total_net_sales=('net_sales', 'sum')
).reset_index()

print(product_sales.head())  # Check the aggregated data

# Create a bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(
        x=product_sales['menu_item'],  # X-axis: Menu items
        y=product_sales['total_net_sales'],  # Y-axis: Total net sales
        text=product_sales['total_quantity_sold'],  # Show quantities sold on hover
        hovertemplate='Total Quantity Sold: %{text}<br>Total Net Sales: $%{y:.2f}<extra></extra>',
        marker=dict(color='steelblue'),
    )
])

# Customize the layout for an executive-level presentation
fig.update_layout(
    title='Total Net Sales by Menu Item',
    xaxis_title='Menu Item',
    yaxis_title='Total Net Sales (USD)',
    template='presentation',  # You can try other templates like 'plotly', 'ggplot2', etc.
    xaxis_tickangle=-45,
    font=dict(size=12),
)

# Show the plot in your browser (optional)
# fig.show()

# Export the plot as an HTML file
fig.write_html('product_mix_analysis.html')

print("Bar chart saved as 'product_mix_analysis.html'")