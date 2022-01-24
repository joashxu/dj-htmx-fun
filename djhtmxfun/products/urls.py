from django.urls import path

from products.views import ProductTableView, ProductHTMxTableView

urlpatterns = [
    path('original/', ProductTableView.as_view(), name='products'),
    path('htmx/', ProductHTMxTableView.as_view(), name='products_htmx'),
]