from django.db import transaction
from django.db.models import F
from django.utils import timezone
from celery import shared_task

from autohouse.models import Autohouse, AutohouseCar
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


@transaction.atomic
def deal_with_supplier(choice, autohouse):
    price = choice.get('price')
    supplier = choice.get('supplier')

    autohouse.balance -= price
    autohouse.full_clean()
    autohouse.save()

    autohouse_car, created = AutohouseCar.objects.get_or_create(
        autohouse=autohouse,
        car=choice['car'],
    )
    if not created and autohouse_car.supplier == choice.get('supplier'):
        autohouse_car.amount += 1
    else:
        autohouse_car.price = price
        autohouse_car.supplier = supplier
    autohouse_car.save()

    supplier.balance += price
    supplier.save()


@shared_task
def autohouse_buying():
    autohouses = Autohouse.objects.all()
    for autohouse in autohouses:
        suitable_cars = Car.objects.filter(**autohouse.prefer_characteristic, is_active=True)
        if suitable_cars.exists():
            choice = best_proposition(suitable_cars)
            deal_with_supplier(choice, autohouse)
