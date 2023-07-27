import os
import csv
import pandas as pd

csv_directory = "school_data/"

csv_files = os.listdir(csv_directory)

combined_data = []

# Loop through each CSV file and process it
for csv_file in csv_files:
    if csv_file.endswith(".csv"):
        # Read the CSV file and skip the first 6 rows
        file_path = os.path.join(csv_directory, csv_file)
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for _ in range(7):
                next(csv_reader)  # Skip the first 7 rows
            # Read the remaining rows
            rows = list(csv_reader)
            # Skip the last 7 rows
            rows = rows[:-7]

            school_year = csv_file.split(".csv")[0][0:9]
            for row in rows:
                row.append(school_year)  # Add the school year to the row
            combined_data.extend(rows)  # Append the rows to the combined_data list

# Add the header row with the column names to the combined data
header_row = [
    'school_name', 'state_name_latest', 'state_name', 'state_abbr', 'school_name_latest',
    'school_id', 'district_name', 'district_id', 'school_type', 'school_wide_title_1',
    'title_1_eligible_latest', 'title_1_eligible_prior', 'total_students',
    'free_lunch_students', 'reduced_lunch_students', 'free_reduced_lunch_students', 'school_year'
]
combined_data.insert(0, header_row)

# Save the combined data to a new CSV file
output_file = 'combined/combined_data.csv'
with open(os.path.join(csv_directory, output_file), 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(combined_data)

# Pandas to read the combined CSV file and move the 'school_year' column to the front
df = pd.read_csv(os.path.join(csv_directory, output_file))
cols = list(df.columns)
cols.remove('school_year')
df = df[['school_year'] + cols]

df.to_csv(os.path.join(csv_directory, output_file), index=False)

print(f"Combined data has been saved to {output_file}.")
