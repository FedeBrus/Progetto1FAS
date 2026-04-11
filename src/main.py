import argparse
import sys
from loader import load_data

def parse_args():
    parser = argparse.ArgumentParser(prog="wals_analyze", description="WALS Data Analysis Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # --- aggregate ---
    parser_aggregate = subparsers.add_parser("aggregate")
    
    parser_aggregate.add_argument("metric", choices=["family", "country"])
    parser_aggregate.add_argument("aggregation", choices=["average", "median"])
    parser_aggregate.add_argument("feature")

    group = parser_aggregate.add_mutually_exclusive_group()
    group.add_argument("-a", "--ascending", action="store_true")
    group.add_argument("-d", "--descending", action="store_true")
    
    parser_aggregate.add_argument("-f", "--filter-family", nargs='+')
    parser_aggregate.add_argument("-c", "--filter-country", nargs='+')

    # --- count ---
    parser_count = subparsers.add_parser("count")

    parser_count.add_argument("metric", choices=["family", "country"])
    parser_count.add_argument("item", choices=["countries", "families", "languages", "feature_value"])

    group = parser_count.add_mutually_exclusive_group()
    group.add_argument("-a", "--ascending", action="store_true")
    group.add_argument("-d", "--descending", action="store_true")
    
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
        
    print(df)

    if args.command == "aggregate":
        pass
    
    elif args.command == "count":
        pass

if __name__ == "__main__":
    main()
