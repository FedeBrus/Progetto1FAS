import pandas as pd

def print_info(df, columns):
    # Da dataframe ad array numpy a lista python
    data = df[columns].drop_duplicates().values.tolist()

    result = []
    for row in data:
        result.append(", ".join(map(str, row)))

    for row in sorted(result):
        print(row)

def print_columns(df):
    # Da dataframe a Index ad array numpy a lista python
    columns = df.columns.values.tolist()
    for col in columns:
        print(col)
