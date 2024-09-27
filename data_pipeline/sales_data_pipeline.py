import os
import pandas as pd
from dotenv import load_dotenv

# grab environment variables
load_dotenv()
STAGING_DATA_DIRECTORY = os.getenv('STAGING_DATA_DIRECTORY')
APP_DATA_DIRECTORY = os.getenv('APP_DATA_DIRECTORY')

# Find the most recent (last modified) CSV file in the staging directory
csv_files = [f for f in os.listdir(STAGING_DATA_DIRECTORY) if f.endswith('.csv')]
if not csv_files:
    raise FileNotFoundError("No CSV files found in the staging directory.")
for file in csv_files:
    print(f"Found CSV file: {file}")

# Get the most recently modified file
latest_csv_file = max([os.path.join(STAGING_DATA_DIRECTORY, f) for f in csv_files], key=os.path.getmtime)

# print the name of the latest CSV file
print(f"\nLatest CSV file found: {latest_csv_file}\n")

# Load the CSV file into a pandas DataFrame
source_data = pd.read_csv(latest_csv_file)

# Ensure the app data directory exists
if not os.path.exists(APP_DATA_DIRECTORY):
    os.makedirs(APP_DATA_DIRECTORY)
    
# Convert the DataFrame to Parquet format with gzip compression
parquet_file_path = os.path.join(APP_DATA_DIRECTORY, 'sales_data.parquet')
source_data.to_parquet(parquet_file_path, compression='brotli')

print(f"\nCSV file {latest_csv_file} successfully converted to Parquet at {parquet_file_path}\n")