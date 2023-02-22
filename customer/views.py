from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Offer
from .serializers import OfferSerializer
from .services import CustomerService


class OfferViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()
    permission_classes = (IsAuthenticated,)
    service = CustomerService()

    def list(self, request, *args, **kwargs):
        customer = self.service.get_customer(request.user.pk)
        qs = self.service.get_active_customer_offers(customer)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)


class OwnStatisticViewSet(
    mixins.ListModelMixin,
    GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    service = CustomerService()

    def list(self, request, *args, **kwargs):
        customer = self.service.get_customer(request.user.pk)
        if self.service.check_car_exists(customer):
            data = self.service.own_statistic(customer)
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': 'You didn`t buy any cars'}, status=status.HTTP_200_OK)
