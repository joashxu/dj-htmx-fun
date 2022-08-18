from django.urls import path

from products.views import ProductTableView, ProductHTMxTableView, ProductHTMxMultiColumTableView


#handler404 = Custom404.as_view()

urlpatterns = [
    path('original/', ProductTableView.as_view(), name='products'),
    path('htmx/', ProductHTMxTableView.as_view(), name='products_htmx'),
    path('multi-col-htmx/', ProductHTMxMultiColumTableView.as_view(), name='products_htmx_multicol'),
]