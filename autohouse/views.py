from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Autohouse, AutohouseCar
from .serializers import AutohouseCarSerializer
from .services import AutohouseService


class AutohouseCarStatisticViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = AutohouseCar.objects.all()
    serializer_class = AutohouseCarSerializer
    filterset_fields = ('autohouse', 'price', 'car')
    search_fields = filterset_fields
    ordering_fields = filterset_fields


class AutohouseStatisticViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Autohouse.objects.all()
    service = AutohouseService()

    def retrieve(self, request, *args, **kwargs):
        data = self.service.autohouse_statistic(self.get_object())
        return Response(data)
