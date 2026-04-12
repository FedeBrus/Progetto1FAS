import argparse
import sys
import loader
import plotter
import stats
import info
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(prog="wals_analyze", description="WALS Data Analysis Tool")
    
    parser.add_argument("-f", "--filter-family", nargs='+')
    parser.add_argument("-c", "--filter-country", nargs='+')
    
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands", required=True)

    # --- COUNT  ---
    parser_count = subparsers.add_parser("count")
    count_subparsers = parser_count.add_subparsers(dest="target", required=True)

    p_countries = count_subparsers.add_parser("countries")
    p_families = count_subparsers.add_parser("families")
    p_features = count_subparsers.add_parser("features")
    p_features.add_argument("feature_id")

    for p in [p_countries, p_families, p_features]:
        p.add_argument("-o", "--order", choices=["ascending", "descending"])

    # --- MAP FEATURE ---
    parser_map_feature = subparsers.add_parser("map_feature")
    parser_map_feature.add_argument("feature_id")

    # --- FAMILY DENSITY ---
    parser_map_family = subparsers.add_parser("map_family")
    parser_map_family.add_argument("family_name")

    # --- INFO ---
    parser_info = subparsers.add_parser("info")
    parser_info.add_argument("item", choices=["features", "countries", "families", "macroareas", "languages", "genii", "subfamilies"])

    return parser.parse_args()

def main():
    args = parse_args()
    dataset_path = "../dataset/features.csv"
    
    try:
        df = loader.load_data(dataset_path)
    except FileNotFoundError as e:
        print(f"Error: dataset file ({dataset_path}) not found")
        sys.exit(1)

    if args.command == "count":
        count_df = stats.count(
            df,
            args.target,
            filter_country=args.filter_country,
            filter_family=args.filter_family,
            order=args.order,
            feature_id=args.feature_id if args.target == "features" else None
        )

        plotter.count_plot(count_df)
        plt.show()

    elif args.command == "map_feature":
        map = stats.map_feature(df, args.feature_id)
        plotter.plot_points_on_map(map)
        plt.show()

    elif args.command == "map_family":
        map = stats.map_family(df, args.family_name)
        plotter.plot_density_on_map(map)
        plt.show()

    
    elif args.command == "info":
        info.print_info(df, args.item)

if __name__ == "__main__":
    main()
