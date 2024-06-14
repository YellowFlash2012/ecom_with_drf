from django_filters import rest_framework as filters
from .models import Product

class ProductsFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = ("category", "brand")

