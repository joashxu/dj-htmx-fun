from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView

from products.models import Product
from products.tables import ProductTable, ProductHTMxTable
from products.filters import ProductFilter


class ProductTableView(SingleTableView):
    table_class = ProductTable
    queryset = Product.objects.all()
    template_name = "products/product_table.html"
    paginate_by = 10


class ProductHTMxTableView(SingleTableMixin, FilterView):
    table_class = ProductHTMxTable
    queryset = Product.objects.all()
    filterset_class = ProductFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            template_name = "products/product_table_partial.html"
        else:
            template_name = "products/product_table_htmx.html"

        return template_name
