from django.db.models import Sum
from rest_framework import serializers

from .models import Customer, Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('id', 'preferred_car', 'price')
        extra_kwargs = {
            'preferred_car': {'required': True},
            'price': {'required': True}
        }

    def validate(self, attrs):
        offer = Offer.objects.filter(**attrs, is_active=True, customer__user=self.context['request'].user)
        if offer.exists():
            raise serializers.ValidationError('You already have such offer')
        return attrs

    def validate_price(self, price):
        customer = Customer.objects.get(user=self.context['request'].user, is_active=True)
        offers = Offer.objects.filter(customer=customer, is_active=True)
        total = offers.annotate(summary=Sum('price')).aggregate(total=Sum('summary'))
        if total.get('total') > customer.balance:
            raise serializers.ValidationError('Total price of your offers is greater than your balance')
        return price

    def create(self, validated_data):
        user = self.context['request'].user
        customer = Customer.objects.get(user=user, is_active=True)
        offer, created = Offer.objects.get_or_create(**validated_data, customer=customer, is_active=True)
        if created:
            return offer
        return self.update(offer, validated_data)

    def update(self, instance, validated_data):
        instance.preferred_car = validated_data.get('preferred_car')
        instance.price = validated_data.get('price')
        instance.save()
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('is_active', 'updated_at', 'created_at')
