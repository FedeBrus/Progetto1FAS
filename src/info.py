import pandas as pd

def get_columns(df, columns):
    print(", ".join(columns) + ":")
    data = df[columns].drop_duplicates()

    result = []
    for row in data.values:
        result.append(", ".join(map(str, row)))

    for row in sorted(result):
      print(row)

def print_headers(df):
    print("Dataset headers:")
    for col in df.columns:
        print(col)
