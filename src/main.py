import argparse
import sys
import loader
import plotter
import stats
import info
import matplotlib.pyplot as plt

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
    parser_map_feature.add_argument("feature_id")

    # --- family density ---
    parser_map_family = subparsers.add_parser("map_family")
    parser_map_family.add_argument("family_name")

    # --- info ---
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

    df = stats.filter(df, "Country_ID", args.filter_country)
    df = stats.filter(df, "Family", args.filter_family)
        
    if args.command == "count_by_countries":
        count_df = stats.count_by_countries(
            df,
            order=args.order,
        )

        plotter.count_plot(count_df)
        plt.show()

    elif args.command == "count_by_families":
        count_df = stats.count_by_families(
            df,
            order=args.order,
        )

        plotter.count_plot(count_df)
        plt.show()

    elif args.command == "count_by_features":
        count_df = stats.count_by_feature(
            df,
            order=args.order,
            feature_id=args.feature_id,
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
        match args.item:
            case "features":
                info.print_features(df)
            case "countries":
                info.print_countries(df)
            case "families":
                info.print_families(df)
            case "macroareas":
                info.print_macroareas(df)
            case "languages":
                info.print_languages(df)
            case "genii":
                info.print_genii(df)
            case "subfamilies":
                info.print_subfamilies(df)

if __name__ == "__main__":
    main()
