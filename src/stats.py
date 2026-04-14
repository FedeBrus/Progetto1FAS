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

def apply_order(df, order, column):
    if order:
        df = df.sort_values(by=column, ascending=order_to_boolean(order))

    return df

def filter(df, column, filter_group=[]):
    query_df = df.copy()

    if filter_group:
        query_df = query_df[query_df[column].isin(filter_group)]

    return query_df

def get_column_values(df, column):
    return list(df[column].unique())

def get_column_chunks(df, column, chunk_size=20):
    all_types = get_column_values(df, column)
    chunks = [all_types[i:i + chunk_size] for i in range(0, len(all_types), chunk_size)]
    
    result = [] 
    
    for chunk in chunks:
        result.append(df[df[column].isin(chunk)])

    return result

def df_to_gdf(df):
    gdf = geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df.Longitude, df.Latitude),
        crs="EPSG:4326"
    )

    return gdf

def count(df, col, by, number, order="descending"):
    query_df = df.copy()

    count_df = (
        query_df
        .groupby(by)[col]
        .nunique()
        .reset_index()
        .rename(columns={col: "Count"})
    )

    count_df = apply_order(count_df, order, "Count")
    count_df = count_df.head(number)
    count_df = count_df.set_index(by)
    return count_df

def map_points(df, metric, identifiers):
    query_df = df.copy()
    query_df = filter(query_df, metric, identifiers)
    query_df = query_df.drop_duplicates(subset=["Language_ID"])
    query_df.set_index(metric)
    return df_to_gdf(query_df)
