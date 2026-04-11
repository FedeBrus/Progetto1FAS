import argparse
import sys
from loader import load_data
import plotter
import stats
import info

def parse_args():
    parser = argparse.ArgumentParser(prog="wals_analyze", description="WALS Data Analysis Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # --- count ---
    parser_count = subparsers.add_parser("count_languages")

    parser_count.add_argument("group", choices=["family", "country", "feature"])
    parser_count.add_argument("-i", "--feature-id", default=None)

    parser_count.add_argument("-d", "--descending", action="store_true")
    
    parser_count.add_argument("-f", "--filter-family", nargs='+')
    parser_count.add_argument("-c", "--filter-country", nargs='+')
    
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
        
    if args.command == "count_languages":
        count_series = stats.count(
            df,
            args.group,
            feature_id=args.feature_id,
            descending=args.descending,
            filter_family=args.filter_family,
            filter_country=args.filter_country
        )

        plotter.count_plot(count_series)
    
    elif args.command == "features":
        info.print_features(df)        

if __name__ == "__main__":
    main()
