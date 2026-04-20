import pandas as pd
import geopandas
import geodatasets
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as cx

def order_to_boolean(order):
    if order == "ascending":
        return True
    elif order == "descending":
        return False

    return False

def get_chunks(df, chunk_size):
    chunks = []
    n_rows = len(df)
    
    for i in range(0, n_rows, chunk_size):
        chunks.append(df.iloc[i : i + chunk_size])
        
    return chunks

def pack_from(df, number):
    top = df.head(number)
    others = df.iloc[number:]

    if not others.empty:
        other_series = pd.Series({"Other": others.sum()})
        languages_by_family = pd.concat([top, other_series])
    else:
        languages_by_family = top

    return languages_by_family

# Ordina column in ordine ascendente o discendente
def apply_order(df, order, column):
    query_df = df.copy()
    query_df = df.sort_values(by=column, ascending=order_to_boolean(order))
    return query_df

# Filtra le righe che in column hanno un qualche valore filter_group
def filter(df, column, filter_group):
    query_df = df.copy()
    query_df = query_df[query_df[column].isin(filter_group)]

    return query_df

# Trasforma un dataframe in un geodataframe
def df_to_gdf(df):
    gdf = geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df.Longitude, df.Latitude),
        crs="EPSG:4326"
    )

    return gdf

def count(df, col, by, order):
    query_df = df.copy()

    count_df = (
        query_df
        .groupby(by)[col]
        .nunique()
        .reset_index()
        .rename(columns={col: "Count"})
    )

    count_df = apply_order(count_df, order, "Count")
    count_df = count_df.set_index(by)
    return count_df

def map_points(df, metric, identifiers):
    query_df = df.copy()
    query_df = filter(query_df, metric, identifiers)
    query_df = query_df.drop_duplicates(subset=["Language_ID"])
    query_df.set_index(metric)
    return df_to_gdf(query_df)
