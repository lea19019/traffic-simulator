import argparse
from tl.simulator import Main
# from tl.optimization_search import run_optimization_search
# from tl.data_generator import run_data_generator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traffic Light Simulator")
    parser.add_argument("-o", "--optimization", action="store_true", help="Run with optimization search")
    parser.add_argument("-d", "--data-generator", action="store_true", help="Run with data generator")

    args = parser.parse_args()

    if args.optimization: print("optimization")
    if args.data_generator: print("data")

    game = Main()
    game.run()