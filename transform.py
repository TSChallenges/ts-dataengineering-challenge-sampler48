# data_engineering/transform.py

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def handle_missing_values(df):
    """
    Handles missing values in the DataFrame by dropping rows with any missing data.

    Parameters:
    - df (pd.DataFrame): Data to clean.

    Returns:
    - pd.DataFrame: Cleaned data.
    """
    df = df.dropna()
    return df



def normalize_data(df, numerical_cols):
    """
    Normalizes specified numerical columns using Min-Max scaling.

    Parameters:
    - df (pd.DataFrame): Data to normalize.
    - numerical_cols (list): List of numerical column names to normalize.

    Returns:
    - pd.DataFrame: Data with normalized columns.
    """
     # Create a copy of the DataFrame
    df = df.copy()
    for num_col in numerical_cols:
        scaler = MinMaxScaler()
        # Change the dtype of the column to float
        df[num_col] = df[num_col].astype(float)
        df[num_col] = scaler.fit_transform(df[[num_col]])
    #df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    print(f"Normalized columns: {', '.join(numerical_cols)}")
    return df


def transform_data(df):
    """
    Transforms the extracted data by cleaning and preparing it for loading.

    Parameters:
    - df (pd.DataFrame): Extracted data.

    Returns:
    - pd.DataFrame: Transformed data.
    """
    if df.empty:
        print("Empty DataFrame received for transformation.")
        return df

    # Step 1: Handle Missing Values
    df = handle_missing_values(df)

    # Step 2: Normalize Numerical Columns
    df = normalize_data(df, numerical_cols=['Age', 'Balance'])

    print("Data transformation completed.")
    return df

