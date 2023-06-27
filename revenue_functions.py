import itertools
from itertools import product
from constants import *

def calculate_total_customer(current_total, organic_growth, sa_count, sa_sale_success_count, base_churn_rate, am_count, am_customer_churn_reduction, am_limit, su_count, su_csat_point_increase, csat_churn_decrease):
    # Assuming churn is at 10% at end of month, first calculate total additions then churn
    # Calculate additions
    total_customers_before_churn = organic_growth + (sa_count * sa_sale_success_count) + current_total

    # Calculate the churn rate
    # Separate the clients with an am and those without.
    am_customers = am_count * am_limit  # Amount of customers with an account manager
    rest_customers = total_customers_before_churn - am_customers  # Amount of customers without an account manager

    if rest_customers < 0:
        # If total account managers have more capacity than total clients then amCustomers are the currentTotal
        rest_customers = 0
        am_customers = current_total

    new_base_churn_rate = base_churn_rate

    if su_count > 0:
        csat_total_point_increase = su_count * (su_csat_point_increase * 100)  # suCSATPointIncrease is given in percentage eg. 0.01 and each percentage point decreases churn rate by csatChurnDecrease
        for i in range(int(csat_total_point_increase)):
            new_base_churn_rate = calc_relative_churn_rate(new_base_churn_rate, csat_churn_decrease)

    total_am_customers = am_customers * (1 - calc_relative_churn_rate(base_churn_rate, am_customer_churn_reduction))
    total_rest_customers = rest_customers * (1 - new_base_churn_rate)

    return total_am_customers + total_rest_customers


def calculate_revenue(total_customers, core_product_cost, am_count, am_limit, am_revenue_increase):
    # Separate the clients with an am and those without.
    am_customers = am_count * am_limit  # Amount of customers with an account manager
    rest_customers = total_customers - am_customers  # Amount of customers without an account manager

    if rest_customers < 0:
        # If total account managers have more capacity than total clients then amCustomers are the currentTotal
        rest_customers = 0
        am_customers = total_customers

    total_am_revenue = (am_customers * core_product_cost) * (1 + am_revenue_increase)
    total_rest_revenue = rest_customers * core_product_cost

    return total_am_revenue + total_rest_revenue

def calc_relative_churn_rate(base_churn_rate, relative_churn_rate):
    relative_reverse = 1 - relative_churn_rate
    return base_churn_rate * relative_reverse

def maximize_revenue_common(number_of_months, total_team_size, combinations_per_month):
    max_revenue = 0
    max_combinations = [None] * number_of_months
    current_customers = CUSTOMERS_DAY_ONE

    total_combinations = len(list(itertools.product(*combinations_per_month)))
    print(f"Number of Months: {number_of_months}")
    print(f"Total Team Size: {total_team_size}")
    print(f"Processing {total_combinations} combination ")

    for month_combinations in product(*combinations_per_month):
        current_customers = CUSTOMERS_DAY_ONE
        monthly_revenue = 0
        for month, (sa_count, am_count, su_count) in enumerate(month_combinations):
            current_customers = calculate_total_customer(current_customers, ORGANIC_GROWTH, sa_count, SA_SALE_SUCCESS_COUNT, BASE_CHURN_RATE, am_count, AM_CUSTOMER_CHURN_REDUCTION, AM_LIMIT, su_count, SU_CSAT_POINT_INCREASE, CSAT_CHURN_DECREASE)
            monthly_revenue = calculate_revenue(current_customers, CORE_PRODUCT_COST, am_count, AM_LIMIT, AM_REVENUE_INCREASE)

            if month == number_of_months - 1 and monthly_revenue > max_revenue:
                max_revenue = monthly_revenue
                max_combinations = month_combinations

    return max_combinations, max_revenue
    
def maximize_revenue(number_of_months, total_team_size):
    combinations_per_month = [list(product(range(total_team_size + 1), repeat=3)) for _ in range(number_of_months)]
    combinations_per_month = [[combo for combo in combinations if sum(combo) == total_team_size] for combinations in combinations_per_month]

    return maximize_revenue_common(number_of_months, total_team_size, combinations_per_month)

def maximize_revenue_am_last_month(number_of_months, total_team_size):
    sa_su_combinations = list(itertools.product(range(total_team_size + 1), repeat=2))
    sa_su_combinations = [combo for combo in sa_su_combinations if sum(combo) == total_team_size]
    sa_su_combinations = [(sa, 0, su) for sa, su in sa_su_combinations]

    all_combinations_last_month = list(itertools.product(range(total_team_size + 1), repeat=3))
    all_combinations_last_month = [combo for combo in all_combinations_last_month if sum(combo) == total_team_size]

    combinations_per_month = [sa_su_combinations] * (number_of_months - 1) + [all_combinations_last_month]

    return maximize_revenue_common(number_of_months, total_team_size, combinations_per_month)

