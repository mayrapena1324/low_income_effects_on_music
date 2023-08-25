import os
import csv


def create_combined_csv(new_csv_file):
    # Create an empty new CSV file and fix headers
    with open(new_csv_file, mode='w', newline='', encoding='utf-8') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(['contest_date', 'event', 'region', 'school', 'tea_code', 'city',
                         'director', 'additional_director', 'accompanist', 'conference',
                         'classification', 'non_varsity_group', 'entry_number', 'title_one',
                         'composer_one', 'title_two', 'composer_two', 'title_three', 'composer_three',
                         'concert_judge', 'concert_judge_1', 'concert_judge_2',
                         'concert_score_1', 'concert_score_two', 'concert_score_three',
                         'concert_final_score', 'sight_reading_judge', 'sight_reading_judge_one',
                         'sight_reading_judge_two', 'sight_reading_score_one',
                         'sight_reading_score_two', 'sight_reading_score_three',
                         'sight_reading_final_score', 'award'])


def append_csv_to_new_file(new_csv_file, file_path):
    with open(new_csv_file, mode='a', newline='', encoding='utf-8') as new_file:
        with open(file_path, mode='r', newline='', encoding='utf-8', errors='replace') as incoming_file:
            reader = csv.reader(incoming_file)
            writer = csv.writer(new_file)

            # Skip the first three rows in the incoming CSV file
            for _ in range(3):
                next(reader)

            # Append the rest of the rows to the new CSV file
            writer.writerows(reader)


UIL_DIRECTORY = "/Users/mayrapena/PycharmProjects/low_income_effects_on_music/uil_data"
CSV_DIRECTORY = os.path.join(os.getcwd(), "csvs")  
os.makedirs(CSV_DIRECTORY, exist_ok=True) 


# Specify the new combined CSV file
combined_csv_file = os.path.join(CSV_DIRECTORY, "combined_uil_scores.csv")

# Create the combined CSV file with the header
create_combined_csv(combined_csv_file)
uil_files = os.listdir(UIL_DIRECTORY)

# Iterate through files in the directory and append them to the combined CSV
for uil_file in uil_files:
    # Check if the file is a CSV file before appending
    if uil_file.endswith('.csv'):
        full_csv_path = os.path.join(UIL_DIRECTORY, uil_file)
        append_csv_to_new_file(combined_csv_file, full_csv_path)
