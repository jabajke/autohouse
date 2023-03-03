from rest_framework import serializers

from .models import AutohouseCar


class AutohouseCarSerializer(serializers.ModelSerializer):
    autohouse = serializers.StringRelatedField()
    car = serializers.StringRelatedField()

    class Meta:
        model = AutohouseCar
        fields = ('id', 'price', 'autohouse', 'car')
