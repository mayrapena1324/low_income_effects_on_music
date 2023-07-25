import os

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website to scrape
base_url = 'https://www.tmea.org/orchestra/honor-orchestra/history/?skip=0&Year_Class=*&Director=&School_Name_op=bw' \
           '&School_Name=&ISD_op=bw&ISD=&submit=Search'
directory = "honor_orchestra_data/"

total_pages = 4

data_list = []

# Loop through each page
for page_num in range(1, total_pages + 1):
    # Send an HTTP GET request to the current page
    url = base_url.format(page_num)
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the HTML elements containing the data you want to scrape (same as before)
        table = soup.find('table')
        data_rows = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):
                row_data.append(cell.text.strip())  # Adjust this based on your specific data
            if row_data:
                data_rows.append(row_data)

        # Append data from this page to the list
        data_list.extend(data_rows)

        print(f"Data from page {page_num} has been scraped.")
    else:
        print(f"Failed to retrieve data from page {page_num}.")

try:
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Create a DataFrame using the data list
    df = pd.DataFrame(data_list, columns=['Year', 'Rank', 'Director', "School", "School District"])

    df.to_csv(os.path.join(directory, 'honor_orchestra_history.csv'), index=False)

    print(f"CSV file has been saved in directory '{directory}'.")
except OSError:
    print(f"Error: Failed to save the CSV file in directory '{directory}'.")


print("Data from all pages has been successfully scraped and saved.")
