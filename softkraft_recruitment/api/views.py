from django.db.models import query
from django.db import models as django_models

from rest_framework import generics
from rest_framework import permissions

from api import enums
from api import models
from api import serializers


class ProductListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = "slug"

    def get_filter_case(self) -> enums.FilterEnum:
        filter_param = self.request.query_params.get("filter")
        if filter_param is None:
            filter_case = enums.FilterEnum.ALL
        elif filter_param == "without_order":
            filter_case = enums.FilterEnum.WITHOUT
        elif filter_param == "with_order":
            filter_case = enums.FilterEnum.WITH
        else:
            filter_case = enums.FilterEnum.ALL
        return filter_case

    def filter_queryset(self, queryset) -> query.QuerySet:
        slug = self.kwargs["slug"]
        filters = {self.lookup_field: slug}
        queryset = queryset.filter(**filters)

        filter_case = self.get_filter_case()
        match filter_case:
            case enums.FilterEnum.ALL:
                queryset = queryset.prefetch_related(
                    django_models.Prefetch(
                        "products",
                        queryset=models.Product.objects.all(),
                        to_attr="filtered_products"
                    )
                )
            case enums.FilterEnum.WITH:
                queryset = queryset.prefetch_related(
                    django_models.Prefetch(
                        "products",
                        queryset=models.Product.objects.filter(
                            order_items__isnull=False
                        ),
                        to_attr="filtered_products"
                    )
                )
            case enums.FilterEnum.WITHOUT:
                queryset = queryset.prefetch_related(
                    django_models.Prefetch(
                        "products",
                        queryset=models.Product.objects.filter(
                            order_items__isnull=True
                        ),
                        to_attr="filtered_products"
                    )
                )

        return queryset
