from django.urls import path, include
from rest_framework import routers
from .views import AutohouseCarStatisticViewSet

router = routers.DefaultRouter()
router.register('cars', AutohouseCarStatisticViewSet)

urlpatterns = [
    path('', include(router.urls))
]
