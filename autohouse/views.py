from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import AutohouseFilter
from .models import Autohouse, AutohouseCar
from .serializers import AutohouseCarSerializer
from .services import AutohouseService


class AutohouseCarStatisticViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = AutohouseCar.objects.all()
    serializer_class = AutohouseCarSerializer
    filterset_class = AutohouseFilter


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


class GeneralAutohouseStatisticViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Autohouse.objects.all()
    service = AutohouseService()

    def list(self, request, *args, **kwargs):
        data = self.service.general_statistic()
        return Response(data)
