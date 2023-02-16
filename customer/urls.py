from django.urls import path, include
from rest_framework import routers

from .views import OfferViewSet

router = routers.DefaultRouter()
router.register('offer', OfferViewSet, basename='offer')

urlpatterns = [
    path('', include(router.urls))
]
