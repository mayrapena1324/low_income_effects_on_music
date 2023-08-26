import os
import csv
import pandas as pd


def get_num_rows_in_original_csvs(directory):
    """Pass in the directory path with csvs. This function will loop through all csvs in a directory and return the
    sum of rows"""
    num_rows_original = 0
    for csv_file in os.listdir(directory):
        if csv_file.endswith(".csv"):
            with open(os.path.join(directory, csv_file), 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                rows = list(csv_reader)
                num_rows_original += len(rows)

    return num_rows_original


def get_num_rows_in_combined_data(directory):
    """Pass in the path to a csv. This function will return the number of rows in the csv."""
    df = pd.read_csv(os.path.join(directory, 'combined/combined_data.csv'))
    num_rows_combined = df.shape[0]
    return num_rows_combined


def assert_no_data_loss(directory):
    """Pass the path of the directory containing csvs. This function calls the get_num_rows_original_csvs
     and asserts the number of rows matches the set test amount."""
    # Get the number of rows in the original CSV files
    num_rows_original = get_num_rows_in_original_csvs(directory)

    # Account for the total number of rows skipped
    total_rows_skipped = 14 * len([file for file in os.listdir(directory) if file.endswith(".csv")])
    num_rows_original -= total_rows_skipped

    # Get the number of rows in the combined DataFrame
    num_rows_combined = get_num_rows_in_combined_data(directory)

    # Assert that the number of rows is the same
    assert num_rows_original == num_rows_combined, f"Number of rows is different. Original: {num_rows_original}, Combined: {num_rows_combined}"

    print("Data has been successfully combined, and no data is lost.")


csv_directory = "school_data/"
output_file = 'combined/combined_data.csv'
OUTPUT_DIRECTORY = 'csvs/general_school_data.csv'

combined_data = []

# Loop through each CSV file and process it
for csv_file in os.listdir(csv_directory):
    if csv_file.endswith(".csv"):
        file_path = os.path.join(csv_directory, csv_file)
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            rows = list(csv_reader)
            # Skip the first 7 and last 7 rows
            rows = rows[7:-7]
            # Grab school year to put in new school_year col
            school_year = csv_file.split(".csv")[0][0:9]
            for row in rows:
                row.append(school_year)
            combined_data.extend(rows)


header_row = [
    'school_name', 'state_name_latest', 'state_name', 'state_abbr', 'school_name_latest',
    'school_id', 'district_name', 'district_id', 'school_type', 'school_wide_title_1',
    'title_1_eligible_latest', 'title_1_eligible_prior', 'total_students',
    'free_lunch_students', 'reduced_lunch_students', 'free_reduced_lunch_students', 'school_year'
]
combined_data.insert(0, header_row)

# Save the combined data to a new CSV file
with open(OUTPUT_DIRECTORY, 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(combined_data)

# Use pandas to read the combined CSV file and move the 'school_year' column to the front
df = pd.read_csv(OUTPUT_DIRECTORY)

school_year_col = df['school_year']
df.drop(columns=['school_year'], inplace=True)
df.insert(0, 'school_year', school_year_col)

df.to_csv(OUTPUT_DIRECTORY, index=False)

print(f"Combined data has been saved to {OUTPUT_DIRECTORY}.")

assert_no_data_loss(csv_directory) 
