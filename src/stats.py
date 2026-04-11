import pandas as pd

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
    

def count_by_countries(df, order=None, filter_country=[]):
    query_df = df.copy()

    if filter_country:
        query_df = query_df[query_df["Country_ID"].isin(filter_country)]

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

    if filter_family:
        query_df = query_df[query_df["Family"].isin(filter_family)]

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

def count_by_feature(df, order=None, feature_id=None):
    query_df = df.copy()

    query_df = query_df[query_df["Parameter_ID"] == feature_id]
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
