from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import AutohouseCar
from .serializers import AutohouseCarSerializer


class AutohouseCarStatisticViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = AutohouseCar.objects.all()
    serializer_class = AutohouseCarSerializer
    filterset_fields = ('autohouse', 'price', 'car')
    search_fields = filterset_fields
    ordering_fields = filterset_fields
