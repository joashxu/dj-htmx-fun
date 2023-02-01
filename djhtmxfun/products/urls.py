from django.urls import path

from products.views import (
    ProductTableView,
    ProductHTMxTableView,
    ProductHTMxMultiColumTableView,
    ProductHTMxBulkActionView,
    response_updateview,
)

# handler404 = Custom404.as_view()

urlpatterns = [
    path("original/", ProductTableView.as_view(), name="products"),
    path("htmx/", ProductHTMxTableView.as_view(), name="products_htmx"),
    path(
        "multi-col-htmx/",
        ProductHTMxMultiColumTableView.as_view(),
        name="products_htmx_multicol",
    ),
    path(
        "bulkaction-htmx/",
        ProductHTMxBulkActionView.as_view(),
        name="products_htmx_bulkaction",
    ),
    path(
        "bulkaction-htmx/update/",
        response_updateview,
        name="products_htmx_bulkaction_update",
    ),
]
