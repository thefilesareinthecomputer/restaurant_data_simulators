'''
# restaurant_details.py

contains the source data for generating "randomized" 
sales data for a theoretical corporate restaurant chain

data is generated according to the following factors:
- menu items
- locations' average annual sales
- regional monthly seasonality distribution
- day of week sales volume distribution
- regional category distribution

next objective:
- create a formula to generate sales data based on the above factors
'''

# corporate restaurant menu organized by category with items and prices
menu = {
    "starters": {
        "Chicken Wings": 12,
        "Shrimp Cocktail": 14,
        "Calamari": 12,
        "Charcuterie Board": 22,
        "Fried Pickles": 8,
        "Bruschetta": 10,
        "Spinach & Artichoke Dip": 9,
        "Baked Brie": 14,
        },
    "salads": {
        "Caesar Salad": 12,
        "Garden Salad": 10,
        "Greek Salad": 14,
        "Cobb Salad": 16,
        "Caprese Salad": 14,
        "Wedge Salad": 12,
        "Tuna Nicoise Salad": 16,
        "Kale & Quinoa Salad": 14,
        "Beet & Goat Cheese Salad": 14,
        },
    "mains": {
        "Burger": 16,
        "Fried Chicken Sandwich": 14,
        "Ribeye Steak": 45,
        "NY Strip Steak": 42,
        "Smoked Beef Rib": 48,
        "Pork Chop": 32,
        "Lamb Chops": 38,
        "Duck Breast": 36,
        "Blackened Chicken": 22,
        "Salmon": 28,
        "Rainbow Trout": 26,
        "Scallops": 32,
        "Lobster Tail": 48,
        "Shrimp Scampi": 28,
        "Grilled Cheese": 12,
        },
    "sides": {
        "French Fries": 6,
        "Sweet Potato Fries": 8,
        "Mashed Potatoes": 6,
        "Mac & Cheese": 10,
        "Onion Rings": 8,
        "Brussels Sprouts": 10,
        "Grilled Asparagus": 10,
        "Side Salad": 6,
        "Garlic Bread": 6,
        "Roasted Fingerling Potatoes": 9,
        "Creamed Spinach": 9,
        },
    "add-ons": {
        "add Bacon": 3,
        "add Avocado": 3,
        "add Fried Egg": 2,
        "add Cheese": 2,
        "add Sauce": 1,
        "add Dressing": 1,
        "add Grilled Chicken": 6,
        "add Grilled Shrimp": 8,
        "add Grilled Salmon": 10,
        "add Grilled NY Strip Steak": 12,
        },
    "desserts": {
        "Cheesecake": 9,
        "Devil's Food Cake": 8,
        "Tiramisu": 10,
        "Ice Cream": 6,
        "Chocolate Mousse": 8,
        "Apple Pie": 8,
        "Flourless Chocolate Torte": 9,
        "Raspberry Tart": 10,
        },
    "beer": {
        "Bell's Two Hearted Ale": 6,
        "Founders All Day IPA": 5,
        "Bell's Oberon Ale": 6,
        "New Belgium Fat Tire": 5,
        "Guinness Draught": 6,
        "Coors Light": 4,
        "Corona Extra": 5,
        "Modelo Especial": 5,
        "Modelo Negra": 5,
        "Hamm's": 3,
        },
    "wine": {
        "Cabernet Sauvignon": 12,
        "Pinot Noir": 10,
        "Chardonnay": 10,
        "Sauvignon Blanc": 10,
        "Merlot": 10,
        "Riesling": 10,
        "Malbec": 12,
        "Rose": 10,
        "Prosecco": 10,
        "Champagne": 15,
        "Port": 12,
        },
    "cocktails": {
        "Old Fashioned": 12,
        "Margarita": 10,
        "Martini": 12,
        "Mojito": 10,
        "Cosmopolitan": 10,
        "Moscow Mule": 10,
        "Negroni": 12,
        "Whiskey Sour": 10,
        },
    "non_alcoholic_beverages": {
        "Water": 0,
        "Bottled Still Water": 6,
        "Bottled Sparkling Water": 6,
        "Coffee": 3,
        "Latte": 5,
        "Cappuccino": 5,
        "Hot Tea": 3,
        "Iced Tea": 2,
        "Coke": 2,
        "Diet Coke": 2,
        "Sprite": 2,
        "Root Beer": 2,
        },
}

# portfolio of corporate restaurant locations and their attributes
locations = {
    "Atlanta": {
        "city": "Atlanta",
        "state": "Georgia",
        "projected_annual_sales": 7_000_000,
        "store_number": 10001,
        "region": "Southeast",
        "average_pay_cooks": 13.50,  # Approx. $28,000 annually
        "average_pay_servers": 7.25,  # Base wage (plus tips)
        },
    "Austin": {
        "city": "Austin",
        "state": "Texas",
        "projected_annual_sales": 9_000_000,
        "store_number": 10002,
        "region": "Southwest",
        "average_pay_cooks": 15.15,  # Approx. $27,500 annually
        "average_pay_servers": 7.25,  # Base wage (plus tips)
        },
    "Boston": {
        "city": "Boston",
        "state": "Massachusetts",
        "projected_annual_sales": 11_000_000,
        "store_number": 10003,
        "region": "Northeast",
        "average_pay_cooks": 17.50,  # Approx. $36,500 annually
        "average_pay_servers": 8.25,  # Base wage (Massachusetts tipped wage)
        },
    "Chicago": {
        "city": "Chicago",
        "state": "Illinois",
        "projected_annual_sales": 14_000_000,
        "store_number": 10004,
        "region": "Midwest",
        "average_pay_cooks": 16.74,  # Approx. $34,810 annually
        "average_pay_servers": 9.48,  # Base wage (Chicago tipped wage)
        },
    "Dallas": {
        "city": "Dallas",
        "state": "Texas",
        "projected_annual_sales": 12_000_000,
        "store_number": 10005,
        "region": "Southwest",
        "average_pay_cooks": 15.60,  # Approx. $26,000 annually
        "average_pay_servers": 7.25,  # Base wage (plus tips)
        },
    "Denver": {
        "city": "Denver",
        "state": "Colorado",
        "projected_annual_sales": 10_000_000,
        "store_number": 10006,
        "region": "West",
        "average_pay_cooks": 17.00,  # Approx. $31,000 annually
        "average_pay_servers": 10.63,  # Colorado tipped wage
        },
    "Detroit": {
        "city": "Detroit",
        "state": "Michigan",
        "projected_annual_sales": 6_000_000,
        "store_number": 10007,
        "region": "Midwest",
        "average_pay_cooks": 14.00,  # Approx. $30,431 annually
        "average_pay_servers": 3.93,  # Michigan tipped wage
        },
    "Houston": {
        "city": "Houston",
        "state": "Texas",
        "projected_annual_sales": 9_000_000,
        "store_number": 10008,
        "region": "Southwest",
        "average_pay_cooks": 14.50,  # Approx. $25,763 annually
        "average_pay_servers": 7.25,  # Base wage (plus tips)
        },
    "Las Vegas": {
        "city": "Las Vegas",
        "state": "Nevada",
        "projected_annual_sales": 14_000_000,
        "store_number": 10009,
        "region": "West",
        "average_pay_cooks": 17.07,  # Approx. $35,500 annually
        "average_pay_servers": 10.50,  # Nevada no tip credit
        },
    "Los Angeles": {
        "city": "Los Angeles",
        "state": "California",
        "projected_annual_sales": 16_000_000,
        "store_number": 10010,
        "region": "West",
        "average_pay_cooks": 18.98,  # Approx. $39,470 annually
        "average_pay_servers": 15.50,  # California no tip credit
        },
    "Miami": {
        "city": "Miami",
        "state": "Florida",
        "projected_annual_sales": 15_000_000,
        "store_number": 10011,
        "region": "Southeast",
        "average_pay_cooks": 16.30,  # Approx. $33,900 annually
        "average_pay_servers": 7.98,  # Florida tipped wage
        },
    "Minneapolis": {
        "city": "Minneapolis",
        "state": "Minnesota",
        "projected_annual_sales": 8_000_000,
        "store_number": 10012,
        "region": "Midwest",
        "average_pay_cooks": 16.12,  # Approx. $33,535 annually
        "average_pay_servers": 10.59,  # Minnesota tipped wage
        },
    "Nashville": {
        "city": "Nashville",
        "state": "Tennessee",
        "projected_annual_sales": 9_000_000,
        "store_number": 10013,
        "region": "Southeast",
        "average_pay_cooks": 12.75,  # Approx. $25,967 annually
        "average_pay_servers": 2.13,  # Base wage (plus tips)
        },
    "New Orleans": {
        "city": "New Orleans",
        "state": "Louisiana",
        "projected_annual_sales": 7_000_000,
        "store_number": 10014,
        "region": "Southeast",
        "average_pay_cooks": 12.20,  # Approx. $23,280 annually
        "average_pay_servers": 2.13,  # Base wage (plus tips)
        },
    "New York": {
        "city": "New York",
        "state": "New York",
        "projected_annual_sales": 18_000_000,
        "store_number": 10015,
        "region": "Northeast",
        "average_pay_cooks": 19.03,  # Approx. $39,580 annually
        "average_pay_servers": 16.00,  # New York tipped wage (NYC)
        },
    "Philadelphia": {
        "city": "Philadelphia",
        "state": "Pennsylvania",
        "projected_annual_sales": 10_000_000,
        "store_number": 10016,
        "region": "Northeast",
        "average_pay_cooks": 14.75,  # Approx. $30,693 annually
        "average_pay_servers": 2.83,  # Pennsylvania tipped wage
        },
    "Portland": {
        "city": "Portland",
        "state": "Oregon",
        "projected_annual_sales": 9_000_000,
        "store_number": 10017,
        "region": "West",
        "average_pay_cooks": 16.33,  # Approx. $33,951 annually
        "average_pay_servers": 14.20,  # Oregon no tip credit
        },
    "San Francisco": {
        "city": "San Francisco",
        "state": "California",
        "projected_annual_sales": 14_000_000,
        "store_number": 10018,
        "region": "West",
        "average_pay_cooks": 19.00,  # Approx. $39,520 annually
        "average_pay_servers": 15.00,  # California no tip credit
        },
    "Seattle": {
        "city": "Seattle",
        "state": "Washington",
        "projected_annual_sales": 12_000_000,
        "store_number": 10019,
        "region": "West",
        "average_pay_cooks": 16.50,  # Approx. $34,320 annually
        "average_pay_servers": 13.50,  # Washington no tip credit
        },
}


regional_monthly_seasonality_distribution = {
    "Midwest": {
        "January": 0.04,
        "February": 0.04,
        "March": 0.06,
        "April": 0.08,
        "May": 0.10,
        "June": 0.12,
        "July": 0.12,
        "August": 0.10,
        "September": 0.09,
        "October": 0.09,
        "November": 0.08,
        "December": 0.08,
        },
    "Northeast": {
        "January": 0.04,
        "February": 0.04,
        "March": 0.06,
        "April": 0.08,
        "May": 0.09,
        "June": 0.10,
        "July": 0.11,
        "August": 0.10,
        "September": 0.09,
        "October": 0.09,
        "November": 0.08,
        "December": 0.08,
        },
    "Southeast": {
        "January": 0.07,
        "February": 0.07,
        "March": 0.09,
        "April": 0.09,
        "May": 0.10,
        "June": 0.10,
        "July": 0.09,
        "August": 0.09,
        "September": 0.07,
        "October": 0.07,
        "November": 0.08,
        "December": 0.08,
        },
    "Southwest": {
        "January": 0.05,
        "February": 0.05,
        "March": 0.07,
        "April": 0.08,
        "May": 0.09,
        "June": 0.09,
        "July": 0.09,
        "August": 0.09,
        "September": 0.08,
        "October": 0.08,
        "November": 0.08,
        "December": 0.08,
        },
    "West": {
        "January": 0.05,
        "February": 0.05,
        "March": 0.07,
        "April": 0.08,
        "May": 0.09,
        "June": 0.10,
        "July": 0.10,
        "August": 0.10,
        "September": 0.09,
        "October": 0.09,
        "November": 0.09,
        "December": 0.09,
        },
}

day_of_week_sales_volume_distribution = {
    "Monday": .09, 
    "Tuesday": .09, 
    "Wednesday": .10, 
    "Thursday": .11, 
    "Friday": .20,  
    "Saturday": .22,  
    "Sunday": .19,  
}

regional_menu_category_preference_distribution = {
    "Midwest": {
        "starters": 0.14,
        "salads": 0.06,
        "mains": 0.30,
        "sides": 0.08,
        "add-ons": 0.05,
        "desserts": 0.07,
        "beer": 0.12,
        "wine": 0.06,
        "cocktails": 0.07,
        "non_alcoholic_beverages": 0.05
        },
    "Northeast": {
        "starters": 0.10,
        "salads": 0.10,
        "mains": 0.22,
        "sides": 0.18,
        "add-ons": 0.05,
        "desserts": 0.05,
        "beer": 0.05,
        "wine": 0.08,
        "cocktails": 0.12,
        "non_alcoholic_beverages": 0.05
        },
    "Southeast": {
        "starters": 0.10,
        "salads": 0.05,
        "mains": 0.30,
        "sides": 0.10,
        "add-ons": 0.10,
        "desserts": 0.05,
        "beer": 0.09,
        "wine": 0.06,
        "cocktails": 0.10,
        "non_alcoholic_beverages": 0.05
        },
    "Southwest": {
        "starters": 0.10,
        "salads": 0.10,
        "mains": 0.30,
        "sides": 0.10,
        "add-ons": 0.05,
        "desserts": 0.05,
        "beer": 0.10,
        "wine": 0.10,
        "cocktails": 0.05,
        "non_alcoholic_beverages": 0.05
        },
    "West": {
        "starters": 0.09,
        "salads": 0.12,
        "mains": 0.28,
        "sides": 0.09,
        "add-ons": 0.05,
        "desserts": 0.05,
        "beer": 0.05,
        "wine": 0.15,
        "cocktails": 0.07,
        "non_alcoholic_beverages": 0.05
        },
}




