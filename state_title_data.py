import pandas as pd
import duckdb

xls = pd.ExcelFile('school_data/title_campus_data.xlsx')
df_2016 = pd.read_excel(xls, sheet_name=0, dtype=str)
df_2017 = pd.read_excel(xls, sheet_name=1, dtype=str)
df_2018 = pd.read_excel(xls, sheet_name=2, dtype=str)
df_2019 = pd.read_excel(xls, sheet_name=3, dtype=str)
df_2020 = pd.read_excel(xls, sheet_name=4, dtype=str)
df_2021 = pd.read_excel(xls, sheet_name=5, dtype=str)

dataframes = [df_2016, df_2017, df_2018, df_2019, df_2020, df_2021]
years = [2016, 2017, 2018, 2019, 2020, 2021]


# Adding a 'year' column to each dataframe using zip
for df, year in zip(dataframes, years):
    df['year'] = year
    df.columns = [col.lower().replace(' ', '_').replace('\n', '_') for col in df.columns]
    df['campus_lowincome_percentage'] = (df['campus_lowincome_percentage'].astype(float) * 100).round(2)

# Combine all dataframes into one
all_data = pd.concat(dataframes, ignore_index=True)

all_data.to_csv('school_data/combined/combined_title_campus_data.csv', index=False)


# Handle buggy df - Removed Region Col
df_2022 = pd.read_excel('school_data/2022_title_campus_data.xlsx', dtype=str, usecols=[1, 2, 3, 4, 5, 6])
df_2022['year'] = 2022
df_2022['Low\nIncome\nPercent'] = (df_2022['Low\nIncome\nPercent'].astype(float) * 100).round(2)
df_2022.to_csv('school_data/combined/combined_title_campus_data.csv', mode='a', header=False, index=False)

# FINAL DF
combined_df = pd.read_csv('school_data/combined/combined_title_campus_data.csv')








# Initialize DuckDB connection
con = duckdb.connect('db.duckdb')

# # Register the DataFrame as a DuckDB table
# con.register('combined_title_data', combined_df)
#
# # Query the table using SQL
# result = con.execute("SELECT * FROM combined_df LIMIT 5;").fetchall()
# print(result)

con.sql('CREATE TABLE integers(i INTEGER)')
con.sql('INSERT INTO integers VALUES (42)')
con.sql('SELECT * FROM integers').show()














##### ISSUES FIXED ###
# THE ISSUE WAS THAT THE OLDER DATA WAS MISSING THE REGION COL!!
# fixed percentages
