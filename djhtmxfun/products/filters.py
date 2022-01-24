from decimal import Decimal

from django.db.models import Q
from django.forms import TextInput
import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method="universal_search",
        label="",
        widget=TextInput(attrs={"placeholder": "Search..."}),
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
