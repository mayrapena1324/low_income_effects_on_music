import os
import camelot
import pandas as pd
import pdfplumber


# Function to remove soft hyphens from a string
def remove_soft_hyphens(text):
    if text is not None:
        return text.replace('\u00AD', "")
    else:
        return ""


output_directory = "all_state_data/all_state_csvs"
pdf_directory = "all_state_data/all_state_pdfs/"
pdf_files = os.listdir(pdf_directory)

all_data_df = pd.DataFrame()

# Loop through each PDF file and process it
for pdf_file in pdf_files:
    full_pdf_path = os.path.join(pdf_directory, pdf_file)
    year = pdf_file[0:4]
    # Use pdfplumber for files 2017 or older
    if int(year) > 2017:
        tables = camelot.read_pdf(full_pdf_path, flavor='stream', pages='all')

        # Concatenate multiple tables from different pages
        df = pd.concat([table.df for table in tables])

    else:
        with pdfplumber.open(full_pdf_path) as pdf:
            pages = pdf.pages

            # Extract table data from each page
            tables = []
            for page in pages:
                table = page.extract_table()
                tables.extend(table)

        df = pd.DataFrame(tables)
        # Add missing column names
        df.columns = ["Student", "School Name", "Event"]
        # Apply the function to all the cells in the DataFrame
        df = df.applymap(remove_soft_hyphens)

    # Add Missing Column Year
    df['Year'] = year

    # Create one large df
    all_data_df = pd.concat([all_data_df, df], ignore_index=True)

# Save the combined DataFrame to a CSV file
all_data_df.to_csv(os.path.join(output_directory, "combined_outstanding_performers.csv"), index=False)
print("Combined CSV file has been saved in your project directory.")
