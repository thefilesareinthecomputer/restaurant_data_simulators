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

requirements:
- data will be calculated from top down as follows:
    - for location in locations:
        - location_monthly_sales_total = location["projected_annual_sales"] * regional_monthly_seasonality_distribution["region"]["month"] for month in months
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











# # 1. Total Sales per Location vs Projected Total Sales and the Delta
# location_sales_summary = {}
# for sale in sales_data:
#     location = sale['location']
#     location_sales_summary[location] = location_sales_summary.get(location, 0) + sale['net_sales']

# print("\n--- Total Sales per Location vs Projected Total Sales ---")
# for location, total_sales in location_sales_summary.items():
#     projected_sales = locations[location]['projected_annual_sales']
#     delta = total_sales - projected_sales
#     print(f"Location: {location}")
#     print(f"  Total Sales: ${total_sales:,.2f}")
#     print(f"  Projected Sales: ${projected_sales:,.2f}")
#     print(f"  Delta: ${delta:,.2f}\n")
    
# print(f"\nTotal number of rows/records created: {len(sales_data)}")







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

# create a date range for the year 2023
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
print(f"Number of days in dataset: {len(days)}\nStart date: {start_date}\nEnd date: {end_date}\n")

# Dictionary to store the projected monthly sales for each location
location_projected_monthly_sales = {}

# Dictionary to store daily sales per location
location_daily_sales = {}

# Dictionary to store daily sales per category for each location
location_category_daily_sales = {}

# Iterate over each location to derive monthly sales totals
for location_name, location in locations.items():
    region = location["region"]
    projected_annual_sales = location["projected_annual_sales"]

    # Initialize daily sales container for each location
    location_daily_sales[location_name] = {}
    location_category_daily_sales[location_name] = {}

    # Retrieve the months directly from the regional_monthly_seasonality_distribution for this region
    for month_name, seasonality_factor in regional_monthly_seasonality_distribution[region].items():
        # Calculate monthly sales based on seasonality factor
        monthly_sales = projected_annual_sales * seasonality_factor

        # Store the result in a dictionary for the location (monthly)
        if location_name not in location_projected_monthly_sales:
            location_projected_monthly_sales[location_name] = {}

        location_projected_monthly_sales[location_name][month_name] = monthly_sales

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
            
            # Store the daily sales in the dictionary
            location_daily_sales[location_name][date_str] = daily_sales

            # Distribute daily sales into categories based on regional preferences
            category_sales = {}
            for category, category_proportion in regional_menu_category_preference_distribution[region].items():
                category_sales[category] = daily_sales * category_proportion
            
            # Store the category sales for that day
            location_category_daily_sales[location_name][date_str] = category_sales
            
            current_date += timedelta(days=1)

# Example output: Print daily sales for a specific location by category
for location, daily_category_sales_data in location_category_daily_sales.items():
    print(f"Location: {location}")
    for date, sales_by_category in daily_category_sales_data.items():
        print(f"  Date: {date}")
        for category, sales in sales_by_category.items():
            print(f"    {category}: ${sales:,.2f}")

# Example output: Print projected monthly sales for each location
for location, sales_data in location_projected_monthly_sales.items():
    print(f"Location: {location}")
    print(f"Projected annual sales: ${locations[location]['projected_annual_sales']:,.2f}")
    for month, sales in sales_data.items():
        print(f"  {month}: ${sales:,.2f}")
'''





























# # Iterate over each location to derive monthly sales totals
# for location_name, location in locations.items():
#     region = location["region"]
#     projected_annual_sales = location["projected_annual_sales"]

#     # Retrieve the months directly from the regional_monthly_seasonality_distribution for this region
#     for month, seasonality_factor in regional_monthly_seasonality_distribution[region].items():
#         # Calculate monthly sales based on seasonality factor
#         monthly_sales = projected_annual_sales * seasonality_factor
        
#         # Store the result in a dictionary for the location
#         if location_name not in location_projected_monthly_sales:
#             location_projected_monthly_sales[location_name] = {}
        
#         location_projected_monthly_sales[location_name][month] = monthly_sales

# # Example output: Print projected monthly sales for each location
# for location, sales_data in location_projected_monthly_sales.items():
#     print(f"Location: {location}")
#     print(f"Projected annual sales: ${locations[location]['projected_annual_sales']:,.2f}")
#     for month, sales in sales_data.items():
#         print(f"  {month}: ${sales:,.2f}")




















# # Function to generate sales data for each location
# def generate_sales_data(start_date, end_date):
#     sales_data = []

#     # Iterate over each location
#     for location_name, location in locations.items():
#         region = location['region']
#         annual_sales = location['projected_annual_sales']
        
#         # Calculate the total sales per month based on seasonality
#         for month, seasonality in regional_monthly_seasonality_distribution[region].items():
#             # Calculate monthly sales target
#             monthly_sales_target = annual_sales * seasonality

#             # Get all the days in the given month
#             month_start_date = datetime(start_date.year, datetime.strptime(month, "%B").month, 1)
#             month_end_date = (month_start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
#             # Split sales by day of the week
#             while month_start_date <= month_end_date:
#                 weekday = month_start_date.strftime("%A")
#                 daily_sales_target = monthly_sales_target * day_of_week_sales_volume_distribution[weekday]
                
#                 # Split daily sales across menu categories based on region's preference
#                 for category, category_weight in regional_menu_category_preference_distribution[region].items():
#                     category_sales_target = daily_sales_target * category_weight
                    
#                     # Split category sales across items
#                     for item_name, item_price in menu[category].items():
#                         # Randomly generate quantity sold based on total category sales
#                         quantity_sold = random.randint(1, int(category_sales_target // item_price))
#                         net_sales = quantity_sold * item_price

#                         # Append the sales record to the dataset
#                         sales_data.append({
#                             'location': location_name,
#                             'region': region,
#                             'date': month_start_date.strftime("%Y-%m-%d"),
#                             'category': category,
#                             'menu_item': item_name,
#                             'quantity_sold': quantity_sold,
#                             'net_sales': net_sales
#                         })
                
#                 month_start_date += timedelta(days=1)
    
#     return sales_data

# # Example Usage
# start_date = datetime(2023, 1, 1)
# end_date = datetime(2023, 12, 31)

# sales_dataset = generate_sales_data(start_date, end_date)

# # Print the first few records to inspect
# for record in sales_dataset[:10]:
#     print(record)



























# def allocate_sales_to_items(sales_target, items):
#     """Distribute sales across items in a category."""
#     sales_allocated = 0
#     item_sales = []
    
#     while sales_allocated < sales_target:
#         # Randomly select an item
#         item, price = random.choice(items)
        
#         # Skip items with price of 0 to avoid division by zero
#         if price == 0:
#             continue
        
#         # Determine max quantity that can be sold
#         max_quantity = int((sales_target - sales_allocated) // price) or 1
#         quantity_sold = random.randint(1, max_quantity)
#         item_sales_value = price * quantity_sold
        
#         # Add item sales to accumulated sales
#         sales_allocated += item_sales_value
        
#         # Store sales data for this item
#         item_sales.append({
#             'item': item,
#             'quantity': quantity_sold,
#             'sales': item_sales_value
#         })
        
#         # Break out if sales target is met or exceeded
#         if sales_allocated >= sales_target:
#             break
    
#     return item_sales

# def generate_sales_per_location(location_data, menu, region_factors):
#     """Generate daily sales data for a given location, broken down by category and item."""
    
#     annual_sales = location_data['projected_annual_sales']
#     region = location_data['region']
    
#     sales_data = []
    
#     # Step 1: Break down annual sales to monthly sales using seasonality distribution
#     for month, seasonal_factor in region_factors['seasonality'].items():
#         monthly_sales = annual_sales * seasonal_factor
        
#         # Step 2: Break down monthly sales into weekly sales
#         for week in range(4):  # Assuming 4 weeks per month for simplicity
#             weekly_sales = monthly_sales / 4
            
#             # Step 3: Allocate weekly sales across days of the week using weekday ratios
#             for day, day_ratio in region_factors['weekday_distribution'].items():
#                 daily_sales = weekly_sales * day_ratio
                
#                 # Step 4: Split daily sales into categories using the regional category distribution
#                 for category, category_ratio in region_factors['category_distribution'].items():
#                     category_sales_target = daily_sales * category_ratio
#                     items_in_category = list(menu[category].items())
                    
#                     # Step 5: Allocate category sales across items
#                     item_sales = allocate_sales_to_items(category_sales_target, items_in_category)
                    
#                     # Step 6: Store results
#                     for sale in item_sales:
#                         sales_data.append({
#                             'location': location_data['city'],
#                             'region': region,
#                             'date': f"2023-{month}-W{week}-{day}",  # Simplified date
#                             'category': category,
#                             'item': sale['item'],
#                             'quantity_sold': sale['quantity'],
#                             'sales': sale['sales']
#                         })
    
#     return sales_data

# all_sales_data = []

# for location_name, location_data in locations.items():
#     # Get regional factors for the current location's region
#     region_factors = {
#         'seasonality': regional_monthly_seasonality_distribution[location_data['region']],
#         'category_distribution': regional_menu_category_preference_distribution[location_data['region']],
#         'weekday_distribution': day_of_week_sales_volume_distribution
#     }
    
#     # Generate sales data for this location
#     location_sales_data = generate_sales_per_location(location_data, menu, region_factors)
    
#     # Append the results to the overall dataset
#     all_sales_data.extend(location_sales_data)

# # Convert to a DataFrame
# df_sales = pd.DataFrame(all_sales_data)

# # Save or display the results
# current_directory = os.path.dirname(__file__)
# # if it doesn't already exist, make a folder called "generated_data" within the current folder
# if not os.path.exists(f"{current_directory}/generated_data"):
#     os.makedirs(f"{current_directory}/generated_data")
# current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
# df_sales.to_csv(f"{current_directory}/generated_data/sales_data_per_location_{current_datetime}.csv", index=False)



































# def generate_sales_dataset(menu, 
#                            locations, 
#                            regional_menu_category_preference_distribution, 
#                            regional_monthly_seasonality_distribution, 
#                            day_of_week_sales_volume_distribution, 
#                            ):
    
#     # Create a list of all days in 2023
#     start_date = datetime(2023, 1, 1)
#     end_date = datetime(2023, 12, 31)
#     days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
#     # Initialize a list to store sales data
#     sales_data = []
    
#     # Iterate over each location
#     for location, location_data in locations.items():
#         region = location_data['region']
#         annual_sales_target = location_data['projected_annual_sales']  # Annual sales target
#         cumulative_sales = 0  # Track cumulative sales for location
        
#         # Step 1: Iterate through each day, calculate sales
#         for day in days:
#             day_name = day.strftime("%A")
#             month_name = day.strftime("%B")
#             weekday_sales_volume = day_of_week_sales_volume_distribution[day_name]
#             seasonal_factor = regional_monthly_seasonality_distribution[region][month_name]
            
#             # Calculate daily sales target (adjusted for seasonality)
#             daily_sales_target = (annual_sales_target / 365) * seasonal_factor
#             cumulative_daily_sales = 0  # Track daily sales
            
#             # Step 2: Split daily sales into AM and PM
#             for day_part in ['am', 'pm']:
#                 day_part_sales_volume = weekday_sales_volume[day_part]
#                 day_part_sales_target = daily_sales_target * day_part_sales_volume
                
#                 # Step 3: Distribute sales across categories in the day part
#                 for category, category_weight in regional_menu_category_preference_distribution[region].items():
#                     category_sales_target = day_part_sales_target * category_weight
                    
#                     # Step 4: Accumulate sales one by one in each category
#                     accumulated_sales = 0
#                     while accumulated_sales < category_sales_target:
#                         # Randomly pick an item from the category
#                         item, price = random.choice(list(menu[category].items()))
                        
#                         # Skip items with a price of 0 (like Water)
#                         if price == 0:
#                             continue
                        
#                         # Sell exactly 1 unit
#                         quantity_sold = 1
#                         item_sales = price * quantity_sold
#                         accumulated_sales += item_sales
                        
#                         # Store the sales data for this item
#                         sale_entry = {
#                             'menu_item': item,
#                             'category': category,
#                             'location': location,
#                             'region': region,
#                             'date': day.strftime("%Y-%m-%d"),
#                             'day_part': day_part.upper(),
#                             'net_sales': item_sales,
#                             'quantity_sold': quantity_sold
#                         }
#                         sales_data.append(sale_entry)
                        
#                         # Log the sale for visibility
#                         print(f"Sold: {quantity_sold} {item}(s) at {location} on {day.strftime('%Y-%m-%d')} ({day_part.upper()}) in {category} - ${item_sales} in sales")
                        
#                         # Stop selling once we hit or surpass the category target
#                         if accumulated_sales >= category_sales_target:
#                             break
            
#     # Group the sales data
#     df = pd.DataFrame(sales_data)
#     df_grouped = df.groupby(['region', 'location', 'date', 'day_part', 'category', 'menu_item']).agg({
#                                  'quantity_sold': 'sum',
#                                  'net_sales': 'sum',
#                              }).reset_index()

#     # Save to CSV
#     current_directory = os.path.dirname(__file__)
#     df_grouped.to_csv(f"{current_directory}/sales_dataset_2023.csv", index=False)

#     print(f"Total sales data generated: {len(sales_data)} rows")
#     print("\nSales data saved to sales_dataset_2023.csv\n")

# # Call the function to generate the dataset
# generate_sales_dataset(menu, 
#                        locations, 
#                        regional_menu_category_preference_distribution, 
#                        regional_monthly_seasonality_distribution, 
#                        day_of_week_sales_volume_distribution, 
#                        )



























# def generate_sales_dataset(menu, 
#                            locations, 
#                            regional_menu_category_preference_distribution, 
#                            regional_monthly_seasonality_distribution, 
#                            day_of_week_sales_volume_distribution, 
#                            ):
    
#     # Create a list of all days in 2023
#     start_date = datetime(2023, 1, 1)
#     end_date = datetime(2023, 12, 31)
#     days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
#     # Initialize a list to store sales data
#     sales_data = []
    
#     # Iterate over each location
#     for location, location_data in locations.items():
#         region = location_data['region']
#         projected_annual_sales = location_data['projected_annual_sales']  # Use projected_annual_sales now
        
#         # Step 2: Break out into daily and day-part sales
#         for day in days:
#             day_name = day.strftime("%A")
#             weekday_sales_volume = day_of_week_sales_volume_distribution[day_name]
            
#             # Iterate through AM/PM splits
#             for day_part in ['am', 'pm']:
#                 day_part_sales_volume = weekday_sales_volume[day_part]
                
#                 # Calculate the total sales for this day part
#                 day_part_sales = projected_annual_sales * day_part_sales_volume / 365  # Daily split for AM/PM

#                 # Step 3: Break into categorical distribution for the region
#                 for category, category_weight in regional_menu_category_preference_distribution[region].items():
#                     category_sales_target = day_part_sales * category_weight
                    
#                     # Get the menu items for this category
#                     items_in_category = list(menu[category].items())
                    
#                     # Step 4: Allocate sales to menu items until the total meets or surpasses the target
#                     accumulated_sales = 0
#                     while accumulated_sales < category_sales_target:
#                         # Randomly select an item from the category
#                         item, price = random.choice(items_in_category)
                        
#                         # Skip items with price of 0 (like Water) to avoid issues
#                         if price == 0:
#                             continue
                        
#                         # Sell 1 unit of the item
#                         quantity_sold = 1
#                         item_sales = price  # Sales from 1 unit

#                         # Add the item sales to the accumulated sales
#                         accumulated_sales += item_sales
                        
#                         # Store the data for the sale
#                         sale_entry = {
#                             'menu_item': item,
#                             'category': category,
#                             'location': location,
#                             'region': region,
#                             'date': day.strftime("%Y-%m-%d"),
#                             'day_part': day_part.upper(),
#                             'net_sales': item_sales,
#                             'quantity_sold': quantity_sold
#                         }
#                         sales_data.append(sale_entry)

#                         # Print a summary of each completed row (item sold)
#                         print(f"Sold: {quantity_sold} {item}(s) at {location} on {day.strftime('%Y-%m-%d')} ({day_part.upper()}) in {category} - ${item_sales} in sales")

#                         # If accumulated sales surpass the target, break out of the loop
#                         if accumulated_sales >= category_sales_target:
#                             break

#     print(f"\nGeneration complete. Total sales data generated: {len(sales_data)} rows\n")
#     print("\nGrouping sales data by location, date, and day part...\n")
    
#     # Create a DataFrame
#     df = pd.DataFrame(sales_data)
    
#     # group
#     df_grouped = df.groupby(['region', 'location', 
#                              'date', 'day_part', 
#                              'category', 'menu_item',]).agg({ 
#                                  'quantity_sold': 'sum',
#                                  'net_sales': 'sum',
#                                  }).reset_index()
    
#     print(df_grouped.head())
#     print(df_grouped.info())
    
#     # Save to CSV
#     current_directory = os.path.dirname(__file__)
#     df_grouped.to_csv(f"{current_directory}/sales_dataset_2023.csv", index=False)

#     print("\nSales data saved to sales_dataset_2023.csv\n")
    
# # Call the function to generate the dataset
# generate_sales_dataset(menu, 
#                        locations, 
#                        regional_menu_category_preference_distribution, 
#                        regional_monthly_seasonality_distribution, 
#                        day_of_week_sales_volume_distribution, 
#                        )







