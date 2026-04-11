import argparse
import sys
from loader import load_data
import plotter
import stats
import info

def parse_args():
    parser = argparse.ArgumentParser(prog="wals_analyze", description="WALS Data Analysis Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # --- count languages by country ---
    parser_count_by_country = subparsers.add_parser("count_by_countries")
    parser_count_by_country.add_argument("-o", "--order", choices=["ascending", "descending"]) 
    parser_count_by_country.add_argument("-f", "--filter-country", nargs='+')

    # --- count languages by family ---
    parser_count_by_family = subparsers.add_parser("count_by_families")
    parser_count_by_family.add_argument("-o", "--order", choices=["ascending", "descending"]) 
    parser_count_by_family.add_argument("-f", "--filter-family", nargs='+')

    # --- count feature values ---
    parser_count_by_feature = subparsers.add_parser("count_by_features")
    parser_count_by_feature.add_argument("feature_id")
    parser_count_by_feature.add_argument("-o", "--order", choices=["ascending", "descending"]) 

    # --- features ---
    parser_features = subparsers.add_parser("features")

    return parser.parse_args()

def main():
    args = parse_args()
    dataset_path = "../dataset/features.csv"
    
    try:
        df = load_data(dataset_path)
    except FileNotFoundError as e:
        print(f"Error: dataset file ({dataset_path}) not found")
        sys.exit(1)
        
    if args.command == "count_by_countries":
        count_df = stats.count_by_countries(
            df,
            order=args.order,
            filter_country=args.filter_country
        )

        plotter.count_plot(count_df)

    elif args.command == "count_by_families":
        count_df = stats.count_by_families(
            df,
            order=args.order,
            filter_family=args.filter_family
        )

        plotter.count_plot(count_df)

    elif args.command == "count_by_features":
        count_df = stats.count_by_feature(
            df,
            order=args.order,
            feature_id=args.feature_id
        )

        plotter.count_plot(count_df)
    
    elif args.command == "features":
        info.print_features(df)        

if __name__ == "__main__":
    main()
