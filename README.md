# Restaurant Chain Sales Dashboard

## Project Description
This is a development project for a restaurant KPI dashboard.
Current features include:
- Generating simulated sales data for analytics pipeline development based on: 
    - pre-programmed menu and location lists 
    - regional and seasonal trends
    - day-of-week fluctuations
- Visualizing sales data in an interactive Dash web app


## Technologies Used
- Python - version 3.11.4
- Pandas
- Plotly
- Pyarrow
- Dash

## Features
- Interactive dashboard for visualizing sales data

## data

### sample of source csv data before conversion to parquet:
```bash
region,location,date,category,menu_item,quantity_sold,net_sales
Southeast,Atlanta,2023-01-01,starters,Charcuterie Board,2,44
Southeast,Atlanta,2023-01-01,starters,Charcuterie Board,1,22
Southeast,Atlanta,2023-01-01,starters,Spinach & Artichoke Dip,2,18
Southeast,Atlanta,2023-01-01,starters,Calamari,5,60
Southeast,Atlanta,2023-01-01,starters,Spinach & Artichoke Dip,3,27
Southeast,Atlanta,2023-01-01,starters,Baked Brie,5,70
Southeast,Atlanta,2023-01-01,starters,Fried Pickles,5,40
Southeast,Atlanta,2023-01-01,starters,Baked Brie,5,70
Southeast,Atlanta,2023-01-01,starters,Spinach & Artichoke Dip,3,27
Southeast,Atlanta,2023-01-01,starters,Baked Brie,2,28
```

### dataframe info:
```bash
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7079822 entries, 0 to 7079821
Data columns (total 7 columns):
 #   Column         Dtype 
---  ------         ----- 
 0   region         object
 1   location       object
 2   date           object
 3   category       object
 4   menu_item      object
 5   quantity_sold  int64 
 6   net_sales      int64 
dtypes: int64(2), object(5)
memory usage: 378.1+ MB
```

### date range: 
- 2023-01-01 to 2023-12-31

### total records: 
- about 7,000,000

### total locations: 
- 15-20

### granularity (each record / row has): 
- total quantity_sold and net_sales for each menu_item per location per day for 2023

### visualizations:
- Total net sales org-wide (a single metric at the top)
- 4 charts in a grid layout:
    - Total net sales per category
    - Total net sales per region
    - Total net sales per location
    - Top 25 menu items org-wide by total net sales (data table)
- Each chart should be able to be clicked / highlighted, and when clicked, the underlying data table at the bottom should filter to show only the data that corresponds to the clicked chart

### slicers:
- slicers for:
    - region
    - location
    - date range (start and end date)
    - menu category
    - menu item
- if no slicers are selected, the dashboard will show the full data

## local setup

### Prerequisites:
- Python 3.11+

### 1. Clone the repository
```bash
git clone https://github.com/thefilesareinthecomputer/restaurant_data_simulators.git
cd restaurant_data_simulators
```
### 2. Set up a virtual environment
```bash
python3.11 -m venv {VENV_NAME}

source {VENV_NAME}/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
- Create a .env file in the root of your project and define the following:
```bash
STAGING_DATA_DIRECTORY=/path/to/staging/data
APP_DATA_DIRECTORY=/path/to/app/data
```

### 5. Run the data pipeline (optional)
- If you want to edit the menu or locations lists, you can do so in the `data_pipeline/restaurant_details.py` file
- Then, to generate new synthetic data, run the following:
```bash
python data_pipeline/sales_data_creator.py
```
- This creates a CSV file in the `STAGING_DATA_DIRECTORY` defined in your .env file
```bash
python data_pipeline/sales_data_pipeline.py
```
- This converts the CSV file to a parquet file and saves it in the `APP_DATA_DIRECTORY` defined in your .env file

### 6. Run the app
```bash
python dash_app/app.py
```

### 7. Open the Dashboard
```bash
Visit http://127.0.0.1:8050/ in your browser.
```