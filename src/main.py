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
    count_subparsers = parser_count.add_subparsers(dest="count_target", required=True)
    
    pc_countries = count_subparsers.add_parser("country")
    pc_families = count_subparsers.add_parser("family")
    pc_features = count_subparsers.add_parser("feature")
    pc_features.add_argument("feature_id")

    parser_count.add_argument("-o", "--order", choices=["ascending", "descending"])
    parser_count.add_argument("-n", "--number", type=int)

    # --- MAP POINTS ---
    parser_map_points = subparsers.add_parser("map_points")
    map_points_subparsers = parser_map_points.add_subparsers(dest="map_points_target", required=True)

    mp_family = map_points_subparsers.add_parser("family")
    mp_family.add_argument("family_names", nargs="+")
    mp_feature = map_points_subparsers.add_parser("feature")
    mp_feature.add_argument("feature_id")

    # --- MAP DENSITY ---
    parser_map_density = subparsers.add_parser("map_density")
    map_density_subparsers = parser_map_density.add_subparsers(dest="map_density_target", required=True)

    md_family = map_density_subparsers.add_parser("family")
    md_family.add_argument("family_names", nargs="+")
    md_feature = map_density_subparsers.add_parser("feature")
    md_feature.add_argument("feature_id")
    md_feature.add_argument("-v", "--feature_value_name")

    # --- INFO ---
    parser_info = subparsers.add_parser("info")
    parser_info.add_argument("columns", nargs="+")

    # -- COLUMNS ---
    parser_cols = subparsers.add_parser("columns")

    return parser.parse_args()

def main():
    args = parse_args()
    dataset_path = "../dataset/features.csv"
    
    try:
        df = loader.load_data(dataset_path)
    except FileNotFoundError as e:
        print(f"Error: dataset file ({dataset_path}) not found")
        sys.exit(1)

    if (args.filter_family):
        df = stats.filter(df, "Family", args.filter_family)
    if (args.filter_country):
        df = stats.filter(df, "Country_ID", args.filter_country)

    if args.command == "count":
        cols = []
        match args.count_target:
            case "family":
                cols = ["Family"]
            case "country":
                cols = ["Country_Name"]
            case "feature":
                cols = ["Code_Name"]
                df = stats.filter(df, "Parameter_ID", [args.feature_id])

        count_df = stats.count(
            df,
            "Language_ID",
            cols,
            order=args.order
        )

        count_df = count_df.head(args.number)

        plotter.count_plot(count_df)
        plt.show()

    elif args.command == "map_points":
        if args.map_points_target == "family":
            map = stats.map_points(
                df,
                "Family",
                args.family_names
            )
            plotter.plot_points_on_map(map, "Family")
            plt.show()
        elif args.map_points_target == "feature":
            map = stats.map_points(
                df,
                "Parameter_ID",
                [args.feature_id]
            )
            plotter.plot_points_on_map(map, "Code_Name")
            plt.show()

    elif args.command == "map_density":
        if args.map_density_target == "family":
            map = stats.map_points(
                df,
                "Family",
                args.family_names
            )
            plotter.plot_density_on_map(map, "Family")
            plt.show()

        elif args.map_density_target == "feature":
            map = stats.map_points(
                df,
                "Parameter_ID",
                [args.feature_id]
            )

            if (args.feature_value_name):
                map = stats.filter(map, "Code_Name", [args.feature_value_name])

            plotter.plot_density_on_map(map, "Code_Name")
            plt.show()
    
    elif args.command == "info":
        info.print_columns(df, args.columns)

    elif args.command == "columns":
        info.print_headers(df)

if __name__ == "__main__":
    main()
