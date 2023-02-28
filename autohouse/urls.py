from django.urls import include, path
from rest_framework import routers

from .views import (AutohouseCarStatisticViewSet, AutohouseStatisticViewSet,
                    GeneralAutohouseStatisticViewSet)

router = routers.DefaultRouter()
router.register('cars', AutohouseCarStatisticViewSet)
router.register('autohouse', AutohouseStatisticViewSet)
router.register('general-statistic', GeneralAutohouseStatisticViewSet)

urlpatterns = [
    path('statistic/', include(router.urls))
]
