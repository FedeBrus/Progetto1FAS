import pandas as pd

def print_features(df):
    for row in df[['Parameter_ID', 'Parameter_Name']].drop_duplicates().itertuples():
        print(f"{row.Parameter_ID}: {row.Parameter_Name}")

def print_countries(df):
    for row in df[['Country_ID', 'Country_Name']].drop_duplicates().itertuples():
        print(f"{row.Country_ID}: {row.Country_Name}")

def print_families(df):
    for row in df['Family'].drop_duplicates():
        print(row)
