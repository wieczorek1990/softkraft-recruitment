from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField("Category", through="ProductCategory", related_name="products")

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.product.pk}, {self.category.pk}"


class Order(models.Model):
    ordered_at = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=256)
    products = models.ManyToManyField(Product, through="OrderItem", related_name="orders")

    def __str__(self) -> str:
        return f"{self.customer_name}, {self.ordered_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"{self.order}, {self.product}, {self.quantity}"
