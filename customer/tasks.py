from celery import shared_task
from django.db.models import F

from autohouse.models import AutohouseCar, AutohouseDiscount
from autohouse.tasks import get_cheapest_car
from customer.models import CustomerPurchaseHistory, Offer


def successful_offer_update(offer, car):
    offer.car = car.car
    offer.price = car.price
    offer.is_active = False
    offer.is_completed = True
    offer.save()


@shared_task
def offer_task():
    cheapest_cars = []
    for offer in Offer.objects.filter(is_active=True):
        suitable_autohouse_car = AutohouseCar.objects.filter(
            **offer.update_keys('car__'),
            price__lte=offer.price,
            is_active=True
        )
        try:
            min_default_price = suitable_autohouse_car.order_by('price')[0]
            cheapest_cars.append(min_default_price)
        except IndexError:
            continue
        discount_cars = AutohouseDiscount.objects.filter(
            **offer.update_keys('autohouse_car__car__'),
            autohouse_car__price__lte=offer.price,
            is_active=True
        )
        try:
            min_discount_price = (
                discount_cars
                .annotate(
                    price=(F('autohouse_car__price') * ((100 - F('discount')) / 100))
                )
                .order_by('price'))[0]
            cheapest_cars.append(min_discount_price)
        except IndexError:
            pass
        cheapest_car = get_cheapest_car(cheapest_cars)
        if cheapest_car:
            successful_offer_update(offer, cheapest_car)
            history, created = CustomerPurchaseHistory.objects.get_or_create(
                customer=offer.customer,
                price=cheapest_car.price,
                car=cheapest_car.car
            )
            if not created:
                history.amount += 1
                history.save()
