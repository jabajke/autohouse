from django_filters import rest_framework as filters

from autohouse.models import AutohouseCar


class AutohouseFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = AutohouseCar
        fields = ('car', 'autohouse')
