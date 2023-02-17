from django.urls import path, include
from rest_framework import routers
from .views import AutohouseStatisticViewSet

router = routers.DefaultRouter()
router.register('cars', AutohouseStatisticViewSet)

urlpatterns = [
    path('', include(router.urls))
]
