import pandas as pd
import geopandas
import geodatasets
import matplotlib.pyplot as plt
import contextily as cx

def get_chunks(df, chunk_size):
    chunks = []
    n_rows = len(df)
    
    for i in range(0, n_rows, chunk_size):
        chunks.append(df.iloc[i : i + chunk_size])
        
    return chunks

def get_list_of(df, column):
    return sorted(df[column].unique().tolist())

def pack_from(df, number):
    keep = number - 1 
    top = df.iloc[:keep]
    others = df.iloc[keep:]

    if not others.empty:
        other_series = pd.Series({"Other": others.sum()})
        languages_by_family = pd.concat([top, other_series])
    else:
        languages_by_family = top

    return languages_by_family

# Filtra le righe che in column hanno un qualche valore filter_group
def filter(df, column, filter_group):
    query_df = df.copy()
    query_df = query_df[query_df[column].isin(filter_group)]

    return query_df
  
def filter_out(df, column, filter_out_group):
    query_df = df.copy()
    query_df = query_df[~query_df[column].isin(filter_out_group)]

    return query_df

# Trasforma un dataframe in un geodataframe
def df_to_gdf(df):
    gdf = geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df.Longitude, df.Latitude),
        crs="EPSG:4326"
    )

    return gdf

def count(df, what, by, sort=False):
    query_df = df.copy()

    count_df = (
        query_df
        .groupby(by)[what]
        .nunique()
    )

    if sort:
      count_df = count_df.sort_values(what, ascending=False)
    
    return count_df

def map_points(df, metric, identifiers):
    query_df = df.copy()
    query_df = filter(query_df, metric, identifiers)
    query_df = query_df.drop_duplicates(subset=["Language_ID"])
    query_df.set_index(metric)
    return df_to_gdf(query_df)
