from input_data.load_customers import load_customers
from input_data.load_vendors import load_vendors
from input_data.products import load_product_spec
from optimize.optimize import start_optimize
from profit import calculate_profit_for_current_start_day
from scenarios.load_scenarios import load_scenarios

from simulation.start_simulation import _run_deterministic_simulation, _filter_out_deliveries_after_end_time, \
    _filter_out_order_out_of_time_scope, run_simulation

DETERMINISTIC = True
SIMULATE_RESULTS = True
NUMBER_OF_DAYS_IN_EACH_RUN = 5
TIME_HORIZON = 15
START_DAY = 1

ADJUST_DELIVERY_ESTIMATE = 0 # Percent, 0 % -> no change


def start_run():

    customers = load_customers()
    product_specs = load_product_spec()

    if SIMULATE_RESULTS:
        scenarios = load_scenarios()
        number_of_runs_in_one_scenario = TIME_HORIZON - NUMBER_OF_DAYS_IN_EACH_RUN + 1

        run_simulation(
            customers=customers,
            number_of_runs_in_one_scenario=number_of_runs_in_one_scenario,
            product_specs=product_specs,
            scenarios=scenarios,
            adjust_delivery_estimate=ADJUST_DELIVERY_ESTIMATE,
            start_day=START_DAY,
            number_of_days_in_each_run=NUMBER_OF_DAYS_IN_EACH_RUN,
            deterministic=DETERMINISTIC
        )

    else:
        vendors = load_vendors(
            path="input_data/deliveries.xlsx",
            adjust_delivery_estimate=ADJUST_DELIVERY_ESTIMATE,
        )
        start_day = START_DAY
        end_day = start_day + NUMBER_OF_DAYS_IN_EACH_RUN
        vendors_with_relevant_deliveries = _filter_out_deliveries_after_end_time(
            vendors=vendors,
            end_day=end_day,
        )
        customers_with_relevant_orders = _filter_out_order_out_of_time_scope(
            customers=customers,
            start_day=start_day,
            end_day=end_day,
        )
        actions = start_optimize(
            vendors=vendors_with_relevant_deliveries,
            customers=customers_with_relevant_orders,
            product_specs=product_specs,
        )
        profit_for_start_day = calculate_profit_for_current_start_day(
            vendors=vendors_with_relevant_deliveries,
            customers=customers_with_relevant_orders,
            product_specs=product_specs,
            actions=actions,
            start_day=start_day,
        )


start_run()
