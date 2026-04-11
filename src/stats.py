import pandas as pd

def count(df, metric, feature_id=None, descending=False, filter_family=[], filter_country=[]):
    column_map = {"family": "Family", "country": "Country_ID", "feature": "Parameter_ID"}
    metric_col = column_map.get(metric)

    query_df = df.copy()

    if filter_family:
        query_df = query_df[query_df["Family"].isin(filter_family)]
    if filter_country:
        query_df = query_df[query_df["Country_ID"].isin(filter_country)]
    
    if metric == "feature" and feature_id:
        query_df = query_df[query_df["Parameter_ID"] == feature_id]

    count_series = query_df.groupby(metric_col)["Language_ID"].nunique()
    
    count_series = count_series.sort_values(ascending=not descending)

    return count_series
