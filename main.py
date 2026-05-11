import argparse

from src import analysis
from src import visualisation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="all", choices=["analyze", "viz", "all"])
    parser.add_argument("--path", default="data/db.csv")
    args = parser.parse_args()
    if args.command == "analyze":
        print("ANALYTICS")
        analysis.run(args.path)
    elif args.command == "viz":
        print("VISUALISATION")
        visualisation.run(args.path)
    elif args.command == "all":
        print("ANALYTICS")
        analysis.run(args.path)
        print("VISUALISATION")
        visualisation.run(args.path)


if __name__ == "__main__":
    main()
