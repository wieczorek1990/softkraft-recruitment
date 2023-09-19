from rest_framework import serializers

from api import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ("id", "name", "price")


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(
        source="filtered_products", many=True, read_only=True
    )

    class Meta:
        model = models.Category
        fields = ("id", "name", "products")
