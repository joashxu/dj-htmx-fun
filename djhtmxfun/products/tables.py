import django_tables2 as tables

from .models import Product


class ProductTable(tables.Table):
    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap4.html"


class ProductHTMxTable(tables.Table):
    class Meta:
        model = Product
        template_name = "tables/bootstrap_htmx_full.html"


class ProductHTMxMultiColumnTable(tables.Table):
    class Meta:
        model = Product
        show_header = False
        template_name = "tables/bootstrap_col_filter.html"


def rows_higlighter(**kwargs):
    # Add highlight class to rows
    # when the product is recently updated.
    # Recently updated rows are in the table
    # selection parameter.
    selected_rows = kwargs["table"].selected_rows
    if selected_rows and kwargs["record"].pk in selected_rows:
        return "highlight-me"
    return ""


class ProductHTMxBulkActionTable(tables.Table):
    # Add a checkbox column to the table.
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, 
                                      attrs={
                                        "td__input": {
                                            "@click": "checkRange"
                                        }
                                     })
    # Status is not orderable
    status = tables.Column(orderable=False)

    class Meta:
        model = Product
        template_name = "tables/bootstrap_htmx_bulkaction.html"
        show_header = False

        # This will put the checkbox column first.
        sequence = ("selection", "...")

        # This will add the highlight class to the rows
        # when the product is recently updated.
        row_attrs = {
            "class": rows_higlighter
        }

        # Additional class for easier styling.
        attrs = {"class": "table checkcolumn-table"}

    def __init__(self, selected_rows=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The selection parameter is a list of product ids
        # that are recently updated.
        self.selected_rows = selected_rows

        return
