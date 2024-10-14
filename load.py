# data_engineering/load.py

import sqlite3
import pandas as pd

def load_data(df, db_name, table_name):
    """
    Loads transformed data into a SQLite database.

    Parameters:
    - df (pd.DataFrame): Transformed data.
    - db_name (str): Name of the SQLite database file.
    - table_name (str): Name of the table to insert data into.

    Returns:
    - None
    """
    if df.empty:
        print("Empty DataFrame received. No data to load.")
        return

    try:
        # Connect to SQLite database (creates the database if it doesn't exist)
          conn = sqlite3.connect(db_name)
          cursor = conn.cursor()
          print(f"Connected to SQLite database: {db_name}")

        # Create a table if it doesn't exist
          create_table_query = generate_create_table_query(df, table_name)
          cursor.execute(create_table_query)
          print(f"Ensured table '{table_name}' exists.")

        # Insert data into the table
          df.to_sql(table_name, conn, if_exists='append', index=False)
          print(f"Inserted {len(df)} records into '{table_name}' table.")

        # Commit and close the connection
          conn.commit()
          conn.close()
          print("Data loading completed and connection closed.")    #
    except sqlite3.Error as e:
          print(f"SQLite error: {e}")
   

def generate_create_table_query(df, table_name):
    """
    Generates a SQL query to create a table based on the DataFrame schema.

    Parameters:
    - df (pd.DataFrame): Data to base the table schema on.
    - table_name (str): Name of the table to create.

    Returns:
    - str: SQL create table query.
    """
    # Enclose table name in double quotes to handle potential SQL keywords
    table_name_quoted = f'"{table_name}"'
    
    columns = []
    for column, dtype in zip(df.columns, df.dtypes):
        # Enclose column names in double quotes as well
        column_quoted = f'"{column}"'
        
        if pd.api.types.is_integer_dtype(dtype):
            sql_type = "INTEGER"
        elif pd.api.types.is_float_dtype(dtype):
            sql_type = "REAL"
        else:
            sql_type = "TEXT"
        columns.append(f"{column_quoted} {sql_type}")

    columns_def = ", ".join(columns)
    create_query = f"CREATE TABLE IF NOT EXISTS {table_name_quoted} ({columns_def});"
    return create_query

   


