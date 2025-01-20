import csv
import pandas as pd

def filter_and_read_columns(csv_file, columns, filter_column, filter_values):
    data = []

    with open(csv_file, 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row[filter_column] in filter_values:
                selected_data = {col: row[col] for col in columns}
                data.append(selected_data)

    return data

# Replace 'BTC-2017min.csv' with the actual path to your CSV file
csv_file_path = 'BTC-2017min.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Convert the datetime column to a datetime object if it's not already
df['date'] = pd.to_datetime(df['date'])

# Group the DataFrame by date and get the last record for each date
last_records_by_date = df.groupby(df['date'].dt.date).last()

# Extract the date values from the DataFrame
filter_values = last_records_by_date['date'].astype(str).tolist()

# Specify the columns to select
selected_columns = ['unix', 'date', 'symbol', 'open', 'high', 'low', 'close', 'Volume BTC', 'Volume USD']

# Specify the output CSV file
output_csv = "step5.csv"

# Filter and write to CSV
result = filter_and_read_columns(csv_file_path, selected_columns, 'date', filter_values)

with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=selected_columns)
    writer.writeheader()
    writer.writerows(result)
