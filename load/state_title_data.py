import pandas as pd

OUTPUT_DIRECTORY = 'csvs/combined_title_campus_data.csv'

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

all_data.to_csv(OUTPUT_DIRECTORY, index=False)


# Handle buggy df - Removed Region Col
df_2022 = pd.read_excel('school_data/2022_title_campus_data.xlsx', dtype=str, usecols=[1, 2, 3, 4, 5, 6])
df_2022['year'] = 2022
df_2022['Low\nIncome\nPercent'] = (df_2022['Low\nIncome\nPercent'].astype(float) * 100).round(2)
df_2022.to_csv(OUTPUT_DIRECTORY, mode='a', header=False, index=False)

# FINAL DF
combined_df = pd.read_csv(OUTPUT_DIRECTORY)
