from django.urls import path

from api import views


urlpatterns = [
    path(
        "categories/<slug:slug>/products/",
        views.ProductListView.as_view(),
        name="products_by_categories"
    ),
]
