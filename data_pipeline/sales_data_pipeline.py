import os
import pandas as pd

current_directory = os.path.dirname(__file__)
project_directory = os.path.join(current_directory, os.pardir)
STAGING_DATA_DIRECTORY = os.path.join(project_directory, 'data_pipeline', 'generated_data')
APP_DATA_DIRECTORY = os.path.join(project_directory, 'dash_app', 'data')

# list all available files in the staging directory
csv_files = [f for f in os.listdir(STAGING_DATA_DIRECTORY) if f.endswith('.csv')]

if not csv_files:
    raise FileNotFoundError("No CSV files found in the staging directory.")

for file in csv_files:
    print(f"Found CSV file: {file}")

# find the most recent (last modified) CSV file in the staging directory
latest_csv_file = max([os.path.join(STAGING_DATA_DIRECTORY, f) for f in csv_files], key=os.path.getmtime)

# print the name of the latest CSV file
print(f"\nLatest CSV file found: {latest_csv_file}\n")

# load CSV file into a pandas dataframe
source_data = pd.read_csv(latest_csv_file)

# ensure the app data directory exists
if not os.path.exists(APP_DATA_DIRECTORY):
    os.makedirs(APP_DATA_DIRECTORY)
    
# convert dataframe to parquet with brotli for best file size
parquet_file_path = os.path.join(APP_DATA_DIRECTORY, 'sales_data.parquet')
source_data.to_parquet(parquet_file_path, compression='brotli')

print(f"\nCSV file {latest_csv_file} successfully converted to Parquet at {parquet_file_path}\n")

def convert_bytes(num):
    """
    This function will convert bytes into a more human-readable format (KB, MB, GB).
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024
        
# print the file sizes of the CSV and Parquet files
csv_size_bytes = os.path.getsize(latest_csv_file)
parquet_size_bytes = os.path.getsize(parquet_file_path)
print(f"CSV File Size: {convert_bytes(csv_size_bytes)}\n")
print(f"Parquet File Size: {convert_bytes(parquet_size_bytes)}\n")
print(f"Parquet File Compression Ratio: {os.path.getsize(latest_csv_file) / os.path.getsize(parquet_file_path):.2f}x\n")
print(f"Parquet size as a percentage of CSV size: {os.path.getsize(parquet_file_path) / os.path.getsize(latest_csv_file) * 100:.2f}%\n")