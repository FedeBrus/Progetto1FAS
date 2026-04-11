import pandas as pd

def average(df, metric, feature, descending=False, filter_family=[], filter_country=[]):
    
    if metric == "family":
        metric = "Family"
    elif metric == "country":
        metric = "Country_ID"

    query_df = df.copy()

    if filter_family:
        query_df = query_df[query_df["Family"].isin(filter_family)]

    if filter_country:
        query_df = query_df[query_df["Country_ID"].isin(filter_country)]
    
    query_df = query_df[query_df["Parameter_ID"] == feature]

    query_df = query_df[[metric, "Number"]]

    query_df = query_df.groupby(metric).mean()

    query_df = query_df.sort_values(by="Number", ascending=not descending)
        
    return query_df 

