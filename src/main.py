import argparse
import sys
from loader import load_data
from stats import *
from plotter import *

def parse_args():
    parser = argparse.ArgumentParser(prog="wals_analyze", description="WALS Data Analysis Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # --- average ---
    parser_average = subparsers.add_parser("average")
    
    parser_average.add_argument("by", choices=["family", "country"])
    parser_average.add_argument("feature")

    parser_average.add_argument("-d", "--descending", action="store_true")
    
    parser_average.add_argument("-f", "--filter-family", nargs='+')
    parser_average.add_argument("-c", "--filter-country", nargs='+')

    # --- count ---
    parser_count = subparsers.add_parser("count")

    parser_count.add_argument("metric", choices=["family", "country"])
    parser_count.add_argument("item", choices=["countries", "families", "languages", "feature_value"])

    parser_count.add_argument("-d", "--descending", action="store_true")
    
    parser_count.add_argument("-f", "--filter-family", nargs='+')
    parser_count.add_argument("-c", "--filter-country", nargs='+')
    
    return parser.parse_args()

def main():
    args = parse_args()
    dataset_path = "../dataset/features.csv"
    try:
        df = load_data(dataset_path)
    except FileNotFoundError as e:
        print(f"Error: dataset file ({dataset_path}) not found")
        sys.exit(1)
        
    if args.command == "average":
        average_frame = average(
            df,
            args.by,
            args.feature,
            descending=args.descending,
            filter_family=args.filter_family,
            filter_country=args.filter_country
        )

        plot_average(average_frame)
    
    elif args.command == "count":
        pass

if __name__ == "__main__":
    main()
