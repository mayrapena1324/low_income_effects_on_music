import pandas as pd

df = pd.read_csv('uil_data/Region29_2018_uil_results.csv',  skiprows=2)
print(df.columns)
