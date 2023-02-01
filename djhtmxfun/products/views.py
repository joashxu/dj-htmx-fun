from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage

from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView

from .models import Product
from .tables import (
    ProductTable,
    ProductHTMxTable,
    ProductHTMxMultiColumnTable,
    ProductHTMxBulkActionTable,
)
from .filters import ProductFilter, ProductUniversalFilter
from .utils import reverse_querystring


class ProductTableView(SingleTableView):
    table_class = ProductTable
    queryset = Product.objects.all()
    template_name = "products/product_table.html"
    paginate_by = 10


class ProductHTMxTableView(SingleTableMixin, FilterView):
    table_class = ProductHTMxTable
    queryset = Product.objects.all()
    filterset_class = ProductUniversalFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            template_name = "products/product_table_partial.html"
        else:
            template_name = "products/product_table_htmx.html"

        return template_name


class CustomPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class ProductHTMxMultiColumTableView(SingleTableMixin, FilterView):
    table_class = ProductHTMxMultiColumnTable
    queryset = Product.objects.all()
    filterset_class = ProductFilter
    paginate_by = 10
    paginator_class = CustomPaginator

    def get_template_names(self):
        if self.request.htmx:
            template_name = "products/product_table_partial.html"
        else:
            template_name = "products/product_table_col_filter.html"

        return template_name


class ProductHTMxBulkActionView(SingleTableMixin, FilterView):
    table_class = ProductHTMxBulkActionTable
    queryset = Product.objects.all()
    filterset_class = ProductUniversalFilter
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            template_name = "products/product_table_partial.html"
        else:
            template_name = "products/product_table_bulkaction.html"

        return template_name

    def get_table_kwargs(self):
        # Get the list of recently updated products.
        # Add the list to the table kwargs.
        kwargs = super().get_table_kwargs()
        selected_rows = self.request.GET.get("selection", None)
        if selected_rows:
            selected_rows = [int(_) for _ in selected_rows.split(",")]
            kwargs["selected_rows"] = selected_rows

        return kwargs



def response_updateview(request):
    if request.method == "POST" and request.htmx:
        # Get the selected products
        selected_products = request.POST.getlist("selection")

        # Check if the activate/deactivate button is pressed
        if request.htmx.trigger_name == "activate":
            # Activate the selected products
            Product.objects.filter(pk__in=selected_products).update(status=Product.Status.ACTIVE)
        elif request.htmx.trigger_name == "deactivate":
            # Deactivate the selected products
            Product.objects.filter(pk__in=selected_products).update(status=Product.Status.INACTIVE)

        # Get the page number
        page = request.POST.get("page", 1)
        page = int(page)

        # Get the sort by column
        sort_by = request.POST.get("sort", None)

        # Get the query
        query = request.POST.get("query", "")

        # Get selection
        selection = ",".join(selected_products)

    # Redirect to table
    return HttpResponseRedirect(
        reverse_querystring("products:products_htmx_bulkaction", 
                            query_kwargs={"page": page, "sort": sort_by,
                                          "query": query, "selection": selection})
    )

