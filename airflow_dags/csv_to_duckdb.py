import duckdb
import pandas as pd
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Connect to DuckDB function
def connect_duckdb(database_path: str):
    return duckdb.connect(database=database_path, read_only=False)

# Task to read a given CSV and insert into DuckDB
def insert_csv_to_duckdb(csv_file_path: str, table_name: str):
    # Connect to DuckDB
    con = connect_duckdb(database_path="path_to_duckdb_file")
    
    # Read the given CSV file
    df = pd.read_csv(csv_file_path)

    # Insert data into DuckDB table using the provided table_name
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM dataframes(df)")

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'start_date': datetime(2023, 8, 25),
    'retries': 1,
}

dag = DAG(
    'csv_to_duckdb_dag',
    default_args=default_args,
    description='A DAG to insert CSV data from multiple directories into DuckDB',
    schedule_interval=None,
)

# Dynamically create tasks based on the CSV files
base_directory = "path_to_base_directory"
for dirpath, dirnames, filenames in os.walk(base_directory):
    for filename in filenames:
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(dirpath, filename)
            
            # Derive table_name, here I'm using the filename without the .csv extension
            # You can adjust this logic as per your requirements
            table_name = os.path.splitext(filename)[0]

            task = PythonOperator(
                task_id=f'insert_{table_name}_to_duckdb',
                python_callable=insert_csv_to_duckdb,
                op_args=[csv_file_path, table_name],  # Passing the file path and table_name to the function
                dag=dag,
            )
