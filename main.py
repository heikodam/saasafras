import argparse
from constants import *
from revenue_functions import maximize_revenue, maximize_revenue_am_last_month
from helper_functions import print_output

def main():
    parser = argparse.ArgumentParser(description='Calculate revenue.')
    parser.add_argument('-t', '--type', help='Type of revenue calculation. Options: "normal", "am_last_month". Default is "normal".')
    parser.add_argument('-m', '--months', type=int, help='Number of months.', required=True)
    parser.add_argument('-s', '--team_size', type=int, help='Total team size.', required=True)
    args = parser.parse_args()

    if args.type == "am_last_month":
        max_combinations, max_revenue = maximize_revenue_am_last_month(args.months, args.team_size)

    else:
        max_combinations, max_revenue = maximize_revenue(args.months, args.team_size)

    print_output(max_combinations, max_revenue)

if __name__ == "__main__":
    main()



