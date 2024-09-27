'''
# sales_data_creator.py

goals:
- generate a dataset of food sales for a theoretical restaurant chain

functionality:
- user sets a date range
- a dataset is generated with the following
- dataset will include 1 aggregated row per each unique combination of: 
    - region
    - location
    - date
    - category
    - menu_item
    - quantity_sold
    - net_sales
    - i.e. 1 grouped row per location per day per menu item with a sum of quantity sold and net sales

methodology:
- data will be calculated from the dictionaries in restaurant_details.py as follows:
    - forecasted annual sales per location are broken down into monthly sales based on regional seasonality ratios for each month
    - monthly sales are further broken down into daily sales based on regional day-of-week sales volume distribution
    - daily sales are then distributed across menu categories based on regional menu category preference distribution
    - finally, sales are allocated semi-randomly to individual menu items within each category for each day until the daily sales target is met
    

'''

import calendar
import os
import pandas as pd
import random
from datetime import datetime, timedelta
from restaurant_details import (locations, 
                                regional_monthly_seasonality_distribution, 
                                day_of_week_sales_volume_distribution, 
                                regional_menu_category_preference_distribution, 
                                menu,
                                )

# Initialize the final dataset to hold sales records
sales_data = []

# Function to simulate sales per category per date
def simulate_sales(location_name, region, date, category, daily_category_sales):
    category_menu_items = menu[category]  # Get the menu items in this category
    
    total_sales = 0
    sales_records = []
    
    # Randomly sell items until we exceed the forecasted category sales for the day
    while total_sales < daily_category_sales:
        # Randomly pick a menu item from the category
        menu_item = random.choice(list(category_menu_items.keys()))
        price = category_menu_items[menu_item]
        
        # Randomly decide how many of this item is sold (e.g., 1-5 items)
        quantity_sold = random.randint(1, 5)
        item_sales = quantity_sold * price
        
        # Check if adding this sale would exceed the category's total sales for the day
        if total_sales + item_sales > daily_category_sales:
            # If it exceeds, stop here and don't add this item
            break
        
        # Otherwise, add the sales to the total and record the sale
        total_sales += item_sales
        sales_records.append({
            'region': region,
            'location': location_name,
            'date': date,
            'category': category,
            'menu_item': menu_item,
            'quantity_sold': quantity_sold,
            'net_sales': item_sales
        })
    
    return sales_records

# Function to set daily sales totals per location
def set_daily_sales_totals():
    # Dictionary to store daily sales per category for each location
    location_category_daily_sales = {}

    # Iterate over each location to derive monthly sales totals
    for location_name, location in locations.items():
        region = location["region"]
        projected_annual_sales = location["projected_annual_sales"]

        # Initialize daily sales container for each location
        location_category_daily_sales[location_name] = {}

        # Retrieve the months directly from the regional_monthly_seasonality_distribution for this region
        for month_name, seasonality_factor in regional_monthly_seasonality_distribution[region].items():
            # Calculate monthly sales based on seasonality factor
            monthly_sales = projected_annual_sales * seasonality_factor

            # Calculate the start and end dates for the current month
            month_start_date = datetime(2023, list(calendar.month_name).index(month_name), 1)
            month_end_date = month_start_date.replace(day=calendar.monthrange(2023, month_start_date.month)[1])

            # Count how many times each weekday appears in the current month
            weekday_counts = {day: 0 for day in day_of_week_sales_volume_distribution.keys()}
            current_date = month_start_date
            while current_date <= month_end_date:
                weekday = calendar.day_name[current_date.weekday()]
                weekday_counts[weekday] += 1
                current_date += timedelta(days=1)

            # Calculate the total sales per weekday in the month
            weekday_sales_totals = {}
            for weekday, proportion in day_of_week_sales_volume_distribution.items():
                weekday_sales_totals[weekday] = monthly_sales * proportion

            # Now distribute the sales per weekday across the dates in the month
            current_date = month_start_date
            while current_date <= month_end_date:
                weekday = calendar.day_name[current_date.weekday()]
                # Sales for this specific day
                daily_sales = weekday_sales_totals[weekday] / weekday_counts[weekday]
                date_str = current_date.strftime("%Y-%m-%d")
                
                # Distribute daily sales into categories based on regional preferences
                category_sales = {}
                for category, category_proportion in regional_menu_category_preference_distribution[region].items():
                    category_sales[category] = daily_sales * category_proportion
                
                # Store the category sales for that day
                location_category_daily_sales[location_name][date_str] = category_sales
                
                current_date += timedelta(days=1)

    return location_category_daily_sales

# Main function to run the simulation
def run_simulation():
    # Step 1: Get daily sales totals per category
    location_category_daily_sales = set_daily_sales_totals()

    # Step 2: For each location, date, and category, simulate sales
    for location_name, daily_sales_data in location_category_daily_sales.items():
        region = locations[location_name]['region']
        for date, category_sales in daily_sales_data.items():
            for category, daily_category_sales in category_sales.items():
                # Simulate the sales for this location, date, and category
                category_sales_records = simulate_sales(location_name, region, date, category, daily_category_sales)
                
                # Append the sales records to the final dataset
                sales_data.extend(category_sales_records)

# Run the simulation
run_simulation()

# convert the sales_data list of dictionaries to a pandas DataFrame
df_sales = pd.DataFrame(sales_data)

print("\n--- Sales Data ---\n")
print(df_sales.head())
print(df_sales.info())

# Save or display the results
current_directory = os.path.dirname(__file__)
# if it doesn't already exist, make a folder called "generated_data" within the current folder
if not os.path.exists(f"{current_directory}/generated_data"):
    os.makedirs(f"{current_directory}/generated_data")
current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
df_sales.to_csv(f"{current_directory}/generated_data/sales_data_per_location_{current_datetime}.csv", index=False)
