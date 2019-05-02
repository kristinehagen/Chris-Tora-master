from typing import List

from input_data.load_customers import Customer, Order, TransportationCost
from input_data.load_vendors import Vendor, Delivery
from input_data.products import ProductType, ProductSpec, Product


def get_vendor_from_id(vendors: List[Vendor], vendor_id: str) -> Vendor:
    return next(
        vendor
        for vendor in vendors
        if vendor.id == vendor_id
    )


def get_delivery_from_del_number(deliveries: List[Delivery], delivery_number: int) -> Delivery:
    return next(
        delivery
        for delivery in deliveries
        if delivery.delivery_number == delivery_number
    )


def get_order_from_id(order_nr: int, orders: List[Order]) -> Order:
    return next(
        order
        for order in orders
        if order.order_number == order_nr
    )


def get_customer_from_id(customers: List[Customer], customer_id: str) -> Customer:
    return next(
        customer
        for customer in customers
        if customer.id == customer_id
    )


def get_product_spec_from_product_type(product_type: ProductType, product_specs: List[ProductSpec]) -> ProductSpec:
    return next(
        product_spec
        for product_spec in product_specs
        if product_spec.product_type == product_type
    )


def get_price_for_product_p(product_type: ProductType, products: List[Product]):
    for product in products:
        if product.product_type == product_type:
            price = product.price
            return price
    raise Exception("Not able to access price for product type " + str(product_type.name))


def order_has_product_p(product_type: ProductType, products: List[Product]):
    for product in products:
        if product.product_type == product_type:
            return True
    return False


def delivery_has_product_p(product_type: ProductType, products: List[Product]):
    for product in products:
        if product.product_type == product_type:
            return True
    return False


def get_transport_price_for_customer_c(product_type: ProductType, transportation_price_per_box: List[TransportationCost], customer_id: str):
    for transportation_price in transportation_price_per_box:
        if transportation_price.product_type == product_type:
            return transportation_price.cost
    raise Exception("Not able to access transportation price for product type " + str(product_type.name) + " for customer " + customer_id)


def get_extra_purchase_price_for_product_p(product_type: ProductType, product_specs: List[ProductSpec]):
    for product_spec in product_specs:
        if product_spec.product_type == product_type:
            extra_price = product_spec.extra_cost
            return extra_price
    raise Exception("Not able to access extra purchase price for product type " + str(product_type.name))
