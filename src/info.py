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

def print_macroareas(df):
    for row in df['Macroarea'].drop_duplicates():
        print(row)

def print_languages(df):
    for row in df[['Language_ID', 'Language_Name']].drop_duplicates().itertuples():
        print(f"{row.Language_ID}: {row.Language_Name}")

def print_macroareas(df):
    for row in df['Genus'].drop_duplicates():
        print(row)

def print_macroareas(df):
    for row in df['Subfamily'].drop_duplicates():
        print(row)
