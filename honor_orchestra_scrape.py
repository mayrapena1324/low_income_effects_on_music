import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'https://www.tmea.org/orchestra/honor-orchestra/history/?skip={}&Year_Class=*&Director=&School_Name_op=bw' \
           '&School_Name=&ISD_op=bw&ISD=&submit=Search'
directory = "honor_orchestra_data/"
total_pages = 4

data_list = []

# Loop through each page
for page_skip in range(0, total_pages):
    url = base_url.format(page_skip * 300)  # Page skip is 300
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')
        data_rows = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):
                row_data.append(cell.text.strip())
            if row_data:
                data_rows.append(row_data)

        data_list.extend(data_rows)

        print(f"Data from page {page_skip + 1} has been scraped.")
    else:
        print(f"Failed to retrieve data from page {page_skip + 1}.")

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
