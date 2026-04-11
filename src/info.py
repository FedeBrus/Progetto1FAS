import pandas as pd

def print_features(df):
    for row in df[['Parameter_ID', 'Parameter_Name']].drop_duplicates().itertuples():
        print(f"{row.Parameter_ID}: {row.Parameter_Name}")
