from celery import shared_task
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from loguru import logger

from autohouse.models import (Autohouse, AutohouseCar,
                              AutoHouseSupplierPurchaseHistory)
from autohouse.utils import Util as autohouse_util
from supplier.models import SupplierCar, SupplierDiscount


def get_cheapest_car(cars):
    cheapest = sorted(cars, key=lambda item: item.price)[0]
    return cheapest


def best_proposition(cars, autohouse):
    cheapest_cars = []
    for car in cars:
        suppliers_car = SupplierCar.objects.filter(
            car=car,
            is_active=True
        )
        if suppliers_car.exists():
            cheapest_supplier_car = suppliers_car.order_by('price').first()
            discounts = SupplierDiscount.objects.filter(
                supplier_car__car=car,
                is_active=True,
                end_date__gte=timezone.now())
            if discounts.exists():
                cheapest_discount_car = (
                    discounts.annotate(price=(F('supplier_car__price') * ((100 - F('discount')) / 100)))
                    .order_by('price')).first()
                if cheapest_discount_car.price < cheapest_supplier_car.price:
                    cheapest_cars.append(cheapest_discount_car)
                    continue
            cheapest_cars.append(cheapest_supplier_car)
    if len(cheapest_cars) > 0:
        return get_cheapest_car(cheapest_cars)
    else:
        logger.info('Suppliers are not able to offer any car for {}'.format(autohouse))


@transaction.atomic
def deal_with_supplier(choice, autohouse):
    if isinstance(choice, SupplierDiscount):
        supplier = choice.supplier_car.supplier
        car = choice.supplier_car.car
    else:
        supplier = choice.supplier
        car = choice.car
    price = choice.price.normalize()
    autohouse.balance -= price
    autohouse.full_clean()
    autohouse.save()
    autohouse_car, created = AutohouseCar.objects.get_or_create(
        autohouse=autohouse,
        car=car,
    )
    if not created and autohouse_car.supplier == supplier:
        autohouse_car.amount += 1
    else:
        autohouse_car.price = price
        autohouse_car.supplier = supplier
    autohouse_car.save()
    supplier.balance += price
    supplier.save()
    AutoHouseSupplierPurchaseHistory.objects.create(
        supplier=supplier,
        autohouse=autohouse,
        car=autohouse_car.car,
        price=price
    )


@shared_task
def autohouse_buying():
    autohouses = Autohouse.objects.all()
    for autohouse in autohouses:
        suitable_cars = autohouse_util.prefer_cars(autohouse.prefer_characteristic)
        if suitable_cars.exists():
            choice = best_proposition(suitable_cars, autohouse)
            if choice is not None:
                deal_with_supplier(choice, autohouse)
        else:
            logger.info('There is no suitable car for {}'.format(autohouse))
