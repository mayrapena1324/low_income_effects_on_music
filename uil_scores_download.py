import os
import time
import csv
import chardet
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def download_csv():
    # Function to download the CSV
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
    # Rename the file
    new_file_name = f"{current_year}_{current_region.replace(' ', '')}_uil_results.csv"
    renamed_file = os.path.join(DOWNLOAD_DICTIONARY, new_file_name)
    os.rename(downloaded_file, renamed_file)

    print(f"File '{new_file_name}' downloaded and renamed.")


# Function to select options in the form
def select_form_options(year, region, event):
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
    # Create an empty new CSV file and write the header row
    new_csv_file = os.path.join(DOWNLOAD_DICTIONARY, "uil_data/combined_uil_scores.csv")
    with open(new_csv_file, mode='w', newline='') as new_file:
        writer = csv.writer(new_file)
        writer.writerow(['Contest Date', 'Event', 'Region', 'School', 'TEA Code', 'City',
                         'Director', 'Additional Director', 'Accompanist', 'Conference',
                         'Classification', 'Non-Varsity Group', 'Entry Number', 'Title 1',
                         'Composer 1', 'Title 2', 'Composer 2', 'Title 3', 'Composer 3',
                         'Concert Judge', 'Concert Judge.1', 'Concert Judge.2',
                         'Concert Score 1', 'Concert Score 2', 'Concert Score 3',
                         'Concert Final Score', 'Sight Reading Judge', 'Sight Reading Judge.1',
                         'Sight Reading Judge.2', 'Sight Reading Score 1',
                         'Sight Reading Score 2', 'Sight Reading Score 3',
                         'Sight Reading Final Score',
                         'Award'])


# Function to append the contents of incoming CSV files
def append_csv_to_new_file(new_csv_file, file_path):
    # Detect the encoding of the incoming CSV file
    with open(file_path, mode='rb') as incoming_file:
        raw_data = incoming_file.read()
        result = chardet.detect(raw_data)
        incoming_encoding = result['encoding']

    # Convert the incoming CSV file to 'utf-8' encoding if it's different
    with open(file_path, mode='r', newline='', encoding=incoming_encoding) as incoming_file:
        with open(new_csv_file, mode='a', newline='', encoding='utf-8') as new_file:
            reader = csv.reader(incoming_file)
            writer = csv.writer(new_file)

            # Skip the first 2 rows in the incoming CSV file (if required)
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


for year in years:
    for region in regions:
        driver.get(URL)
        try:
            select_form_options(year, region, event)  # Select options without specifying a contest
            downloaded_file = download_csv()
            time.sleep(10)  # Respecting Site

            append_csv_to_new_file(new_csv_file='uil_data/combined_uil_scores.csv', file_path=downloaded_file)
            rename_csv(current_year=year, current_region=region)

        except NoSuchElementException:
            print(f"{region} skipped.")
            pass


print("All CSV files downloaded and appended into 'new_file.csv'.")
driver.quit()
