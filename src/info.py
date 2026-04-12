import pandas as pd

def print_info(df, item):
    cols = []
    match item:
        case "languages":
            cols = ["Language_ID", "Language_Name"]
        case "families":
            cols = ["Family"]
        case "subfamilies":
            cols = ["Subfamily"]
        case "genii":
            cols = ["Genus"]
        case "features":
            cols = ["Parameter_ID", "Parameter_Name"]
        case "countries":
            cols = ["Country_ID", "Country_Name"]
        case "macroareas":
            cols = ["Macroarea"]

    print_tuples(df, cols)

def print_tuples(df, cols):
    for row in df[cols].drop_duplicates().values.tolist():
        print(", ".join(map(str, row)))
