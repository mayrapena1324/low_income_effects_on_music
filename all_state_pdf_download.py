import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


DOWNLOAD_DICTIONARY = "/Users/mayrapena/PycharmProjects/low_income_effects_on_music/all_state_data/all_state_pdfs"
URL = "https://www.uiltexas.org/music/archives"
YEARS = ["2017", "2018", "2019", "2021", "2022", "2023"]


def set_up_driver():
    """Configures the driver for pdf download"""
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DICTIONARY,
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })

    configured_driver = webdriver.Chrome(options=options)
    return configured_driver


def download_outstanding_performer():
    """Opens uiltexas.org and downloads the Outstanding Performer pdf files based on the years specified in the YEARS
    list. Saves them in the all_state_data directory."""
    driver = set_up_driver()
    for year in YEARS:
        try:
            driver.get(URL)
            driver.find_element(By.LINK_TEXT, f"{year} Outstanding Performer").click()
            time.sleep(2)
        except NoSuchElementException:
            # Skip if file not available
            print(f" No {year} Outstanding Performer file available.")
            pass
    driver.quit()


download_outstanding_performer()
