from django.db.models import Count, F, Sum

from .models import Customer, CustomerPurchaseHistory, Offer


class CustomerService:
    def get_active_customer_offers(self, customer):
        qs = Offer.objects.filter(is_active=True, customer=customer)
        return qs

    def get_customer(self, user_pk):
        return Customer.objects.get(user=user_pk)

    def own_statistic(self, customer):
        offers = Offer.objects.filter(customer=customer)
        history = CustomerPurchaseHistory.objects.filter(customer=customer)
        data = dict(
            offers_count=offers.count(),
            car_bought=history.count(),
            money_spent=history
            .annotate(total_price=Sum('price') * F('amount'))
            .aggregate(total=Sum('total_price'))['total'],
            lovely_brand=history.values('car__brand')
            .annotate(brand_count=Count('car__brand'))
            .order_by('-brand_count')
            .first()['car__brand']
        )
        return data

    def check_car_exists(self, customer):
        history = CustomerPurchaseHistory.objects.filter(customer=customer)
        if history.exists():
            return True
        return False
