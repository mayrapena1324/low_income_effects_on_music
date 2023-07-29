import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def download_csv():
    """Downloads and returns the csv. Throws an error if the csv takes too long."""
    driver.find_element(By.CSS_SELECTOR, '#export-csv').click()
    # Wait for the file to finish downloading
    timeout = 30
    downloaded_file = os.path.join(DOWNLOAD_DICTIONARY, "UilCSRPublicReport.csv")
    start_time = time.time()
    while not os.path.exists(downloaded_file):
        time.sleep(1)
        if time.time() - start_time > timeout:
            raise TimeoutError("File download took too long.")
    return downloaded_file


def rename_csv(current_year, current_region):
    """Rename the csv with the current year and region"""
    new_file_name = f"{current_year}_{current_region.replace(' ', '')}_uil_results.csv"
    renamed_file = os.path.join(DOWNLOAD_DICTIONARY, new_file_name)
    os.rename(downloaded_file, renamed_file)

    print(f"File '{new_file_name}' downloaded and renamed.")


def select_form_options(year, region, event):
    """Fills out the UIL form with the year, region, and event."""
    year_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="yr"]'))
    region_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="reg"]'))
    event_select = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="ev"]'))

    # Select the options in the dropdowns
    year_select.select_by_visible_text(year)
    time.sleep(2)  # Pause for 2 seconds
    region_select.select_by_visible_text(region)
    time.sleep(2)  # Pause for 2 seconds
    event_select.select_by_visible_text(event)

    # Submit the form to populate the next dropdown
    driver.find_element(By.CSS_SELECTOR, 'form[name="f3"]').submit()


def create_combined_csv():
    """Creates the new csv and inserts the header """
    new_csv_file = os.path.join(DOWNLOAD_DICTIONARY, "uil_data/combined/combined_uil_scores.csv")
    with open(new_csv_file, mode='w', newline='') as new_file:
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
    return new_csv_file


def append_csv_to_new_file(new_csv_file, file_path):
    with open(new_csv_file, mode='a', newline='') as new_file:
        with open(file_path, mode='r', newline='') as incoming_file:
            reader = csv.reader(incoming_file)
            writer = csv.writer(new_file)

            # Skip the first 3 rows in the incoming CSV file
            for _ in range(3):
                next(reader)

            # Append the rest of the rows to the new CSV file
            writer.writerows(reader)


DOWNLOAD_DICTIONARY = "/Users/mayrapena/PycharmProjects/low_income_effects_on_music/uil_data"
URL = "https://www.texasmusicforms.com/csrrptuilpublic.asp"

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("prefs", {
    "download.default_directory": DOWNLOAD_DICTIONARY,
    "download.prompt_for_download": False
})

driver = webdriver.Chrome(options=options)

years = ["2018", "2019", "2021", "2022", "2023"]  # Skipped 2020 because COVID Canceled the contest
regions = [f"Region {x}" for x in range(1, 34)]  # Add all the available regions here
regions.append("Region 76")  # Edge case
event = "Band"  # This option includes all other data. Story about Why Orchestra Option does not work for all Regions

combined_csv_file = create_combined_csv()

for year in years:
    for region in regions:
        driver.get(URL)
        try:
            select_form_options(year, region, event)  # Select options without specifying a contest
            downloaded_file = download_csv()
            time.sleep(10)  # Respecting Site

            append_csv_to_new_file(combined_csv_file, downloaded_file)
            rename_csv(current_year=year, current_region=region)

        except NoSuchElementException:
            print(f"{region} skipped.")
            pass

    print("All CSV files downloaded and appended into 'combined_uil_scores.csv'.")
    driver.quit()
