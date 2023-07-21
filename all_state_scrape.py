import time
import tabula
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

DOWNLOAD_DICTIONARY = "/Users/mayrapena/PycharmProjects/low_income_effects_on_music/all_state_data"
URL = "https://www.uiltexas.org/music/archives"
YEARS = ["2017", "2018", "2019", "2021", "2022", "2023"]


def set_up_driver():
    # Set up the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "detach": True,
        "download.default_directory": DOWNLOAD_DICTIONARY,
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })

    configured_driver = webdriver.Chrome(options=options)
    return configured_driver


def download_outstanding_performer():
    driver = set_up_driver()
    driver.get(URL)


download_outstanding_performer()
