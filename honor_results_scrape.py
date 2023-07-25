import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_class_from_year(year_str):
    # Split the year_str by whitespace
    year_parts = year_str.split()
    if len(year_parts) > 1:
        # Return the last part as class information
        return " ".join(year_parts[1:])
    else:
        # Return empty string if no class information found
        return ""


def scrape_honor_data(base_url, num_pages, directory, file_name):
    data_list = []

    for page_skip in range(0, num_pages):
        url = base_url.format(page_skip * 300)  # Page skip is 300
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            table = soup.find('table')
            data_rows = []
            for i, row in enumerate(table.find_all('tr')):
                # Always skip the first row
                if i == 0:
                    continue

                row_data = []
                for cell in row.find_all('td'):
                    cell_text = cell.text.strip()
                    if cell_text:  # Skip empty cells
                        row_data.append(cell_text)
                if row_data:
                    data_rows.append(row_data)

            data_list.extend(data_rows)

            print(f"Data from page {page_skip + 1} has been scraped.")
        else:
            print(f"Failed to retrieve data from page {page_skip + 1}.")

    try:
        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)

        df = pd.DataFrame(data_list, columns=['Year', 'Rank', 'Director', "School", "School District"])

        # Add a new column "Class" extracted from the "Year" column
        df['Class'] = df['Year'].apply(extract_class_from_year)

        # Modify the "Year" column to keep only the year value
        df['Year'] = df['Year'].apply(lambda year_str: year_str.split()[0])

        # Reorder the columns to have "Class" right after "Year"
        cols = df.columns.tolist()
        cols.insert(1, cols.pop(cols.index('Class')))
        df = df.reindex(columns=cols)

        df.to_csv(os.path.join(directory, f'{file_name}_history.csv'), index=False)

        print(f"CSV file has been saved in directory '{directory}'.")
    except OSError:
        print(f"Error: Failed to save the CSV file in directory '{directory}'.")

    print("Data from all pages has been successfully scraped and saved.")


# Create a function (base_url, total pages, directory)

orchestra_url = 'https://www.tmea.org/orchestra/honor-orchestra/history/?skip={' \
                '}&Year_Class=*&Director=&School_Name_op=bw' \
               '&School_Name=&ISD_op=bw&ISD=&submit=Search'

band_url = 'https://www.tmea.org/band/honor-band/history/?skip={' \
           '}&Year_Class=*&Director=&School_Name_op=bw&School_Name=&ISD_op=bw&ISD=&submit=Search'
directory = "honor_data/"
orchestra_pages = 4
band_pages = 5

# scrape band
scrape_honor_data(base_url=band_url, num_pages=band_pages, directory=directory, file_name='honor_band')

# scrape orchestra
scrape_honor_data(base_url=orchestra_url, num_pages=orchestra_pages, directory=directory, file_name='honor_orchestra')
