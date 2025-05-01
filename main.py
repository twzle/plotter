import yaml
import argparse
import time


from src.stats import load_stats_from_yaml
from src.plotter import Plotter


def parse_args():
    parser = argparse.ArgumentParser(description="Process a file path.")

    parser.add_argument("-f", "--file", required=True, help="Path to the file")

    args = parser.parse_args()
    
    return args



def main():
    try:
        print("\n--------------\n")
        print("Plotter executed...\n")
        args = parse_args()
        stats = load_stats_from_yaml(args.file)
    except Exception as e:
        print(e)
    else:
        plotter = Plotter(stats)
        plotter.run()


if __name__ == "__main__":
    main()
