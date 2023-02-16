from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Offer
from .serializers import OfferSerializer


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

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(is_active=True, customer__user=request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(data=serializer.data)
