from django.urls import path, include
from rest_framework import routers

from .views import OfferViewSet, OwnStatisticViewSet

router = routers.DefaultRouter()
router.register('offer', OfferViewSet, basename='offer')
router.register('me/statistic', OwnStatisticViewSet, basename='statistic')

urlpatterns = [
    path('', include(router.urls)),
]
