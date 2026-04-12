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


def count_by_countries(df, order=None, filter_country=[]):
    query_df = df.copy()
    count_df = (
        query_df
        .groupby(["Country_ID", "Country_Name"])["Language_ID"]
        .nunique()
        .reset_index()
        .rename(columns={"Language_ID": "Language_Count"})
    )

    count_df = apply_order(count_df, order, "Language_Count")

    count_df = count_df.set_index("Country_Name")

    return count_df

def count_by_families(df, order=None, filter_family=[]):
    query_df = df.copy()

    count_df = (
        query_df
        .groupby(["Family"])["Language_ID"]
        .nunique()
        .reset_index()
        .rename(columns={"Language_ID": "Language_Count"})
    )
    
    count_df = apply_order(count_df, order, "Language_Count")

    count_df = count_df.set_index("Family")

    return count_df

def count_by_feature(df, order=None, feature_id=None, filter_family=[], filter_country=[]):
    query_df = df.copy()        
    query_df = filter(query_df, "Parameter_ID", [feature_id])
    count_df = (
        query_df
        .groupby(["Code_ID", "Code_Name"])["Language_ID"]
        .nunique()
        .reset_index()
        .rename(columns={"Language_ID": "Language_Count"})
    )

    count_df = apply_order(count_df, order, "Language_Count")

    count_df = count_df.set_index("Code_Name")

    return count_df

def df_to_gdf(df):
    gdf = geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df.Longitude, df.Latitude),
        crs="EPSG:4326"
    )

    return gdf

def map_feature(df, feature_id):
    query_df = df.copy()
    query_df = filter(query_df, "Parameter_ID", [feature_id])
    return df_to_gdf(query_df)

def map_family(df, family_name):
    query_df = df.copy()
    query_df = filter(query_df, "Family", [family_name])
    return df_to_gdf(query_df)

