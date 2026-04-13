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

def count(df, metric, order=None, feature_id=None, filter_family=[], filter_country=[]):
    query_df = df.copy()
    
    query_df = filter(query_df, "Family", filter_family)
    query_df = filter(query_df, "Country_ID", filter_country)

    if feature_id:
        query_df = filter(query_df, "Parameter_ID", [feature_id])
    
    cols = []
    match metric:
        case "families":
            cols = ["Family"]
        case "countries":
            cols = ["Country_Name"]
        case "features":
            cols = ["Code_Name"]

    count_df = (
        query_df
        .groupby(cols)["Language_ID"]
        .nunique()
        .reset_index()
        .rename(columns={"Language_ID": "Language_Count"})
    )

    count_df = apply_order(count_df, order, "Language_Count")

    count_df = count_df.set_index(cols)

    return count_df

def df_to_gdf(df):
    gdf = geopandas.GeoDataFrame(
        df,
        geometry=geopandas.points_from_xy(df.Longitude, df.Latitude),
        crs="EPSG:4326"
    )

    return gdf

def map_points(df, metric, identifier):
    query_df = df.copy()
    
    filter_by = ""
    match metric:
        case "family":
            filter_by = "Family"
        case "feature":
            filter_by = "Parameter_ID"

    query_df = filter(query_df, filter_by, [identifier])
    query_df.set_index(filter_by)
    return df_to_gdf(query_df)

def map_family(df, family_name):
    query_df = df.copy()
    query_df = filter(query_df, "Family", [family_name])
    query_df = query_df.drop_duplicates(subset=["Language_ID"])
    return df_to_gdf(query_df)

def map_all_languages_by_family(df):
    query_df = df.copy()
    query_df = query_df.drop_duplicates(subset=["Language_ID"])
    query_df.set_index("Family")
    return df_to_gdf(query_df)

def get_family_chunks(gdf, chunk_size=20):
    all_families = sorted(gdf['Family'].unique())
    chunks = [all_families[i:i + chunk_size] for i in range(0, len(all_families), chunk_size)]
    return [gdf[gdf['Family'].isin(chunk)] for chunk in chunks]
