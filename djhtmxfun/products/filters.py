import math
from decimal import Decimal

from django.db.models import Q
from django.forms import TextInput
import django_filters

from .models import Product


class SearchInput(TextInput):
    input_type = "search"


class ProductUniversalFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method="universal_search",
        label="",
        widget=SearchInput(attrs={"placeholder": "Search..."}),
    )

    class Meta:
        model = Product
        fields = ["query"]

    def universal_search(self, queryset, name, value):
        if value.replace(".", "", 1).isdigit():
            value = Decimal(value)
            return Product.objects.filter(Q(price=value) | Q(cost=value))

        return Product.objects.filter(
            Q(name__icontains=value) | Q(category__icontains=value)
        )


class ProductFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label="")
    name = django_filters.CharFilter(label="", lookup_expr="istartswith")
    category = django_filters.CharFilter(label="", lookup_expr="istartswith")
    price = django_filters.NumberFilter(label="", method="filter_decimal")
    cost = django_filters.NumberFilter(label="", method="filter_decimal")
    status = django_filters.ChoiceFilter(label="", choices=Product.Status.choices)

    class Meta:
        model = Product
        fields = ["id", "name", "category", "price", "cost", "status"]

    def filter_decimal(self, queryset, name, value):
        # For price and cost, filter based on
        # the following property:
        # value <= result < floor(value) + 1

        lower_bound = "__".join([name, "gte"])
        upper_bound = "__".join([name, "lt"])

        upper_value = math.floor(value) + Decimal(1)

        return queryset.filter(**{lower_bound: value,
                                  upper_bound: upper_value})
