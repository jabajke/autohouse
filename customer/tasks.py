from celery import shared_task
from django.db.models import F
from loguru import logger

from autohouse.models import AutohouseCar, AutohouseDiscount
from autohouse.tasks import get_cheapest_car
from customer.models import CustomerPurchaseHistory, Offer


def offer_update(offer, cheapest_car):
    if isinstance(cheapest_car, AutohouseDiscount):
        car = cheapest_car.autohouse_car.car
        autohouse = cheapest_car.autohouse_car.autohouse
    else:
        car = cheapest_car.car
        autohouse = cheapest_car.autohouse
    offer.car = car
    offer.price = cheapest_car.price
    offer.is_active = False
    offer.is_completed = True
    offer.customer.balance -= cheapest_car.price
    offer.customer.save()
    offer.save()
    return car, autohouse


@shared_task
def offer_task():
    cheapest_cars = []
    offers = Offer.objects.filter(is_active=True)
    if offers.exists():
        for offer in offers:
            suitable_autohouse_car = AutohouseCar.objects.filter(
                **offer.update_keys('car__'),
                price__lte=offer.price,
                is_active=True
            )
            cheapest_default_car = suitable_autohouse_car.order_by('price').first()
            if not cheapest_default_car:
                logger.info('There is no car for {}'.format(offer))
                continue
            cheapest_cars.append(cheapest_default_car)
            discount_cars = AutohouseDiscount.objects.filter(
                **offer.update_keys('autohouse_car__car__'),
                autohouse_car__price__lte=offer.price,
                is_active=True
            )
            if discount_cars.exists():
                min_discount_price = (
                    discount_cars
                    .annotate(
                        price=(F('autohouse_car__price') * ((100 - F('discount')) / 100))
                    )
                    .order_by('price')).first()
                cheapest_cars.append(min_discount_price)
            if len(cheapest_cars) > 0:
                cheapest_car = get_cheapest_car(cheapest_cars)
                car, autohouse = offer_update(offer, cheapest_car)
                CustomerPurchaseHistory.objects.create(
                    customer=offer.customer,
                    price=cheapest_car.price,
                    car=car,
                    autohouse=autohouse
                )
    else:
        logger.info('No active offers')
