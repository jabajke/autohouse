from django.urls import include, path
from rest_framework import routers

from .views import AutohouseCarStatisticViewSet, AutohouseStatisticViewSet

router = routers.DefaultRouter()
router.register('statistic/cars', AutohouseCarStatisticViewSet)
router.register('statistic/autohouse', AutohouseStatisticViewSet)

urlpatterns = [
    path('', include(router.urls))
]
