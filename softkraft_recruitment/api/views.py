from rest_framework import generics
from rest_framework import permissions

from api import models
from api import serializers


class ProductListView(generics.ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = "slug"

    def filter_queryset(self, queryset):
        queryset = queryset.filter(**{self.lookup_field: self.kwargs["slug"]})

        with_order = self.request.query_params.get("filter")
        if with_order is None:
            pass
        elif with_order == "without_order":
            queryset = queryset.filter(products__orders__isnull=True).distinct()
        else:
            pass

        return queryset
