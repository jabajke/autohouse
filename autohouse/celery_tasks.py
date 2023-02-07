from celery import shared_task
from django.db.models import F
from django.utils import timezone

from autohouse.models import Autohouse
from main.models import Car
from supplier.models import SupplierCar, SupplierDiscount


def best_proposition(cars):
    for car in cars:
        discounts = SupplierDiscount.objects.filter(
            supplier_car__car=car,
            is_active=True,
            end_date__gte=timezone.now())
        if discounts.exists():
            min_discount_price = (
                discounts.annotate(price=(F('supplier_car__price') * ((100 - F('discount')) / 100)))
                .order_by('price'))[0]
        else:
            min_discount_price = None
        min_default_price = SupplierCar.objects.filter(
            car=car,
            is_active=True,
        ).order_by('price')[0]

        if min_discount_price is not None:
            if min_discount_price.price < min_default_price.price:
                return {
                    'supplier': min_discount_price.supplier_car.supplier,
                    'price': min_discount_price.price,
                    'car': min_discount_price.supplier_car.car
                }
        return {
            'supplier': min_default_price.supplier,
            'price': min_default_price.price,
            'car': min_default_price.car
        }


def autohouse_buying():
    autohouses = Autohouse.objects.all()
    for autohouse in autohouses:
        suitable_cars = Car.objects.filter(**autohouse.prefer_characteristic, is_active=True)
        if suitable_cars.exists():
            choice = best_proposition(suitable_cars)
