import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_class_from_year(year_str):
    year_parts = year_str.split()
    if len(year_parts) > 1:
        return " ".join(year_parts[1:])
    else:
        return ""


def scrape_honor_data(base_url, num_pages, save_directory, file_name):
    data_list = []

    for page_skip in range(0, num_pages):
        url = base_url.format(page_skip * 300)  # Page skip is 300
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table')

            # Use list comprehension to extract data rows and skip the first row
            data_rows = [row.find_all('td') for i, row in enumerate(table.find_all('tr')) if i > 0]
            # Use list comprehension to build row_data and skip empty cells
            data_rows = [[cell.text.strip() for cell in row]
                         for row in data_rows if any(cell.text.strip() for cell in row)]

            data_list.extend(data_rows)

            print(f"Data from page {page_skip + 1} has been scraped.")
        else:
            print(f"Failed to retrieve data from page {page_skip + 1}.")

    try:
        os.makedirs(save_directory, exist_ok=True)

        df = pd.DataFrame(data_list, columns=['Year', 'Rank', 'Director', "School", "School District"])

        df['Class'] = df['Year'].apply(extract_class_from_year)
        df['Year'] = df['Year'].apply(lambda year_str: year_str.split()[0])

        cols = df.columns.tolist()
        cols.insert(1, cols.pop(cols.index('Class')))
        df = df.reindex(columns=cols)

        df.to_csv(os.path.join(save_directory, f'{file_name}_history.csv'), index=False)

        print(f"CSV file has been saved in directory '{save_directory}'.")
    except OSError:
        print(f"Error: Failed to save the CSV file in directory '{save_directory}'.")

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
scrape_honor_data(
    base_url=band_url,
    num_pages=band_pages,
    save_directory=directory,
    file_name='honor_band')

# scrape orchestra
scrape_honor_data(base_url=orchestra_url,
                  num_pages=orchestra_pages,
                  save_directory=directory,
                  file_name='honor_orchestra')
