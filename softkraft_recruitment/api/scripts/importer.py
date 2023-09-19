import csv

from django.utils import text

from api import models


def orders():
    with open("api/csv/orders.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            order_id, product_id, quantity, customer = (
                row["order_id"], row["product_id"],
                row["quantity"], row["customer"]
            )
            yield order_id, product_id, quantity, customer


def products():
    with open("api/csv/products.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_, name, price, category_name = (
                row["id"], row["name"],
                row["price"], row["category name"]
            )
            yield id_, name, price, category_name


def run() -> None:
    print("Products")
    for id_, name, price, category_name in products():
        product, _ = models.Product.objects.get_or_create(name=name, price=price)
        categories = category_name.split(";")
        for category in categories:
            slug = text.slugify(category)
            category, _ = models.Category.objects.get_or_create(name=category, slug=slug)
            models.ProductCategory.objects.get_or_create(product=product, category=category)

    print("Orders.")
    for order_id, product_id, quantity, customer_name in orders():
        models.Order.objects.get_or_create(id=order_id, defaults=dict(customer_name=customer_name))
    for order_id, product_id, quantity, customer_name in orders():
        models.OrderItem.objects.get_or_create(order_id=order_id, product_id=product_id, quantity=quantity)
