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
- Flask

## Features
- Interactive dashboard for visualizing sales data

## data

### sample of source csv data before conversion to parquet:
```
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
```
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
- Total net sales
- Total net sales per category
- Total net sales per location
- Top 25 menu items org-wide by total net sales (data table)
- Top 5 menu items per region by total net sales (bar chart)
- Top 5 sales weeks per location by total net sales (heatmap)
- Total net sales by category (bar chart)

### slicers:
- region
- location
- date range (start and end date)
- menu category
- menu item

## setup

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
