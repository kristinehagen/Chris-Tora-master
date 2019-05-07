from typing import List

from helpers import order_has_product_p, get_transport_price_for_customer_c, get_price_for_product_p, \
    get_extra_purchase_price_for_product_p, delivery_has_product_p
from input_data.load_customers import Customer, TransportationCost
from input_data.load_vendors import Vendor
from input_data.products import ProductSpec, ProductType, Product
from optimize.variables import Variables


def create_objective_function(
        vendors: List[Vendor],
        customers: List[Customer],
        solver,
        variables: Variables,
        product_specs: List[ProductSpec],
        number_of_scenarios: int,
):
    objective = solver.Objective()

    _set_x_objective(
        x_vars=variables.x,
        customers=customers,
        vendors=vendors,
        product_specs=product_specs,
        objective=objective,
        number_of_scenarios=number_of_scenarios,
    )

    _set_y_objective(
        y_vars=variables.y,
        customers=customers,
        product_specs=product_specs,
        objective=objective,
        number_of_scenarios=number_of_scenarios,
    )

    _set_o_objective(
        customers=customers,
        vendors=vendors,
        o_vars=variables.o,
        objective=objective,
        number_of_scenarios=number_of_scenarios,
    )

    return objective


def _set_x_objective(x_vars, customers: List[Customer], vendors: List[Vendor], product_specs: List[ProductSpec], objective, number_of_scenarios: int):
    for s in range(number_of_scenarios):
        for v, vendor in enumerate(vendors):
            for d, delivery in enumerate(vendor.deliveries):
                for c, customer in enumerate(customers):
                    for o, order in enumerate(customer.orders):
                        for p, product_spec in enumerate(product_specs):
                            if order_has_product_p(product_type=product_spec.product_type, products=order.demand) \
                                    and delivery_has_product_p(product_type=product_spec.product_type, products=order.demand):

                                sales_price = get_price_for_product_p(product_type=product_spec.product_type, products=order.demand)
                                transport_cost = get_transport_price_for_customer_c(
                                    product_type=product_spec.product_type,
                                    transportation_price_per_box=customer.transportation_price_per_box,
                                    customer_id=customer.id
                                )
                                if customer.out_of_country:
                                    customs_cost = product_spec.customs_cost
                                    coefficient = sales_price - transport_cost - customs_cost
                                else:
                                    coefficient = sales_price - transport_cost

                                objective.SetCoefficient(x_vars[s][v][d][c][o][p], coefficient)


def _set_y_objective(y_vars, customers: List[Customer], product_specs: List[ProductSpec], objective, number_of_scenarios: int):
    for s in range(number_of_scenarios):
        for c, customer in enumerate(customers):
            for o, order in enumerate(customer.orders):
                for p, product_spec in enumerate(product_specs):
                    if order_has_product_p(product_type=product_spec.product_type, products=order.demand):

                        transport_price = get_transport_price_for_customer_c(
                            product_type=product_spec.product_type,
                            transportation_price_per_box=customer.transportation_price_per_box,
                            customer_id=customer.id
                        )
                        price = get_price_for_product_p(product_type=product_spec.product_type, products=order.demand)
                        extra_cost = get_extra_purchase_price_for_product_p(
                            product_type=product_spec.product_type,
                            product_specs=product_specs
                        )
                        if customer.out_of_country:
                            customs_cost = product_spec.customs_cost
                            coefficient = price - transport_price - extra_cost - customs_cost
                        else:
                            coefficient = price - transport_price - extra_cost

                        objective.SetCoefficient(y_vars[s][c][o][p], coefficient)


# Oslo cost
def _set_o_objective(customers, vendors, o_vars, objective, number_of_scenarios: int):
    for s in range(number_of_scenarios):
        for v, vendor in enumerate(vendors):
            for d, delivery in enumerate(vendor.deliveries):
                for c, customer in enumerate(customers):
                    for o, order in enumerate(customer.orders):
                        objective.SetCoefficient(o_vars[s][v][d][c][o], -1)




