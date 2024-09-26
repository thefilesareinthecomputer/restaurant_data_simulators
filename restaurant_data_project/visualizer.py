import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
PROJECT_DIRECTORY = os.getenv('PROJECT_DIRECTORY')

# Load the CSV file into a DataFrame
data_path = os.path.join(PROJECT_DIRECTORY, 'restaurant_data_project', 'generated_data')
file_name = f'{data_path}/sales_data_per_location_2024-09-26_16-50-15.csv'
df = pd.read_csv(file_name)

# Aggregate sales data by menu item (sum quantity_sold and net_sales)
product_sales = df.groupby('menu_item').agg(
    total_quantity_sold=('quantity_sold', 'sum'),
    total_net_sales=('net_sales', 'sum')
).reset_index()

print(product_sales.head())  # Check the aggregated data