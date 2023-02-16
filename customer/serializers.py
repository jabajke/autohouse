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
        customer = Customer.objects.get(user=self.context['request'].user, is_active=True)
        if customer.balance < attrs.get('price'):
            raise serializers.ValidationError('Current balance is lower than price')
        return attrs

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
