def print_output(max_combinations, max_revenue):
    if max_combinations is None:
        print("No valid team distribution found that maximizes revenue in the last month.")
    else:
        print(f"\nThe optimal team distribution for each month that maximizes revenue in the last month is:")
        for month, (sa_count, am_count, su_count) in enumerate(max_combinations, start=1):
            print(f"Month {month}: SA_COUNT = {sa_count}, AM_COUNT = {am_count}, SU_COUNT = {su_count}")
        print(f"\nThe maximum possible revenue in the last month with this distribution is: {max_revenue}")