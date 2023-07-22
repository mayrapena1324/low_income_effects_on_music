import os
import camelot
import pandas as pd

# Directory path containing all the PDF files
pdf_directory = "all_state_data/all_state_pdfs/"

# List all the files in the directory
pdf_files = os.listdir(pdf_directory)

# Loop through each PDF file and process it
for pdf_file in pdf_files:
    # Generate the full file path
    full_pdf_path = os.path.join(pdf_directory, pdf_file)

    # Load the PDF and extract tables
    tables = camelot.read_pdf(full_pdf_path, flavor='stream', pages='all')

    # Concatenate multiple tables from different pages
    df = pd.concat([table.df for table in tables])

    # Generate the output CSV file name
    output_file = os.path.join("all_state_data/all_state_csvs/", os.path.splitext(pdf_file)[0] + ".csv")

    # Save the extracted data as a CSV file
    df.to_csv(output_file, index=False)
    print(f"CSV file '{output_file}' has been saved in your project directory.")



