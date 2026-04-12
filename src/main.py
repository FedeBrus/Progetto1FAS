import argparse
import sys
from loader import load_data
import plotter
import stats
import info

def parse_args():
    parser = argparse.ArgumentParser(prog="wals_analyze", description="WALS Data Analysis Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    parser.add_argument("-f", "--filter-family", nargs='+')
    parser.add_argument("-c", "--filter-country", nargs='+')

    # --- count languages by country ---
    parser_count_by_country = subparsers.add_parser("count_by_countries")
    parser_count_by_country.add_argument("-o", "--order", choices=["ascending", "descending"]) 

    # --- count languages by family ---
    parser_count_by_family = subparsers.add_parser("count_by_families")
    parser_count_by_family.add_argument("-o", "--order", choices=["ascending", "descending"]) 

    # --- count feature values ---
    parser_count_by_feature = subparsers.add_parser("count_by_features")
    parser_count_by_feature.add_argument("feature_id")
    parser_count_by_feature.add_argument("-o", "--order", choices=["ascending", "descending"]) 

    # --- map feature ---
    parser_map_feature = subparsers.add_parser("map_feature")

    # --- info ---
    parser_info = subparsers.add_parser("info")
    parser_info.add_argument("item", choices=["features", "countries", "families"])

    return parser.parse_args()

def main():
    args = parse_args()
    dataset_path = "../dataset/features.csv"
    
    try:
        df = load_data(dataset_path)
    except FileNotFoundError as e:
        print(f"Error: dataset file ({dataset_path}) not found")
        sys.exit(1)

    df = stats.filter(df, args.filter_family, args.filter_country)
        
    if args.command == "count_by_countries":
        count_df = stats.count_by_countries(
            df,
            order=args.order,
        )

        plotter.count_plot(count_df)

    elif args.command == "count_by_families":
        count_df = stats.count_by_families(
            df,
            order=args.order,
        )

        plotter.count_plot(count_df)

    elif args.command == "count_by_features":
        count_df = stats.count_by_feature(
            df,
            order=args.order,
            feature_id=args.feature_id,
        )

        plotter.count_plot(count_df)

    elif args.command == "map_feature":
        map = stats.map()
        plotter.plot_on_map(map)
    
    elif args.command == "info":
        match args.item:
            case "features":
                info.print_features(df)
            case "countries":
                info.print_countries(df)
            case "families":
                info.print_families(df)

if __name__ == "__main__":
    main()
