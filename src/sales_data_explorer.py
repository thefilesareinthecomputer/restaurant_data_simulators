'''
# sales_dataset_cleaner.py
'''

import os
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load the sales_dataset_2023.csv file into a dataframe
current_directory = os.path.dirname(__file__)
df = pd.read_csv(f"{current_directory}/generated_data/sales_data_per_location_2024-09-26_14-59-25.csv")

print("\n--- Initial DataFrame Head ---\n")
print(df.head())
print("\n--- DataFrame Info ---\n")
print(df.info())

# Print total count of rows with null values per column
print("\n--- Count of null values in each column ---\n")
print(df.isnull().sum())

# Total quantity sold and dollar net_sales per menu_item
df_items = df.groupby('menu_item').agg({
    'quantity_sold': 'sum',
    'net_sales': 'sum'
}).sort_values(by='quantity_sold', ascending=False)

print("\n--- Total quantity sold per menu_item (Top 100) ---\n")
print(df_items.head(100))

# Total dollar net_sales per menu_item (already sorted by quantity, but you can sort by net_sales if needed)
df_items_sorted_by_sales = df_items.sort_values(by='net_sales', ascending=False)

print("\n--- Total dollar net_sales per menu_item (Top 100) ---\n")
print(df_items_sorted_by_sales.head(100))

# Total quantity and dollar net_sales per category
df_category = df.groupby('category').agg({
    'quantity_sold': 'sum',
    'net_sales': 'sum'
}).sort_values(by='quantity_sold', ascending=False)

print("\n--- Total quantity sold per category ---\n")
print(df_category)

# Total dollar net_sales per category (sorted by net_sales)
df_category_sorted_by_sales = df_category.sort_values(by='net_sales', ascending=False)

print("\n--- Total dollar net_sales per category ---\n")
print(df_category_sorted_by_sales)

# Total net_sales per location
df_location = df.groupby('location').agg({
    'net_sales': 'sum'
}).sort_values(by='net_sales', ascending=False)

print("\n--- Total net_sales per location ---\n")
print(df_location)