from celery import shared_task
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from supplier.models import SupplierCar, SupplierDiscount

from .models import Autohouse, AutohouseCar
from .utils import Util as autohouse_util


def get_cheapest_car(cars):
    cars = list(filter(lambda item: item is not None, cars))
    if cars:
        cheapest = sorted(cars, key=lambda item: item.price)[0]
        return cheapest
    return False


def best_proposition(cars):
    min_discount_price_list = []
    min_default_price_list = []
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

        min_discount_price_list.append(min_discount_price)
        min_default_price_list.append(min_default_price)

    cheapest_discount_car = get_cheapest_car(min_discount_price_list)
    cheapest_default_car = get_cheapest_car(min_default_price_list)

    if cheapest_discount_car:
        if cheapest_discount_car.price < cheapest_default_car.price:
            data = {
                'supplier': cheapest_discount_car.supplier,
                'price': cheapest_discount_car.price,
                'car': cheapest_discount_car.car
            }
    else:
        data = {
            'supplier': cheapest_default_car.supplier,
            'price': cheapest_default_car.price,
            'car': cheapest_default_car.car
        }
    return data


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
        suitable_cars = autohouse_util.concatenate_json(autohouse.prefer_characteristic)
        if suitable_cars.exists():
            choice = best_proposition(suitable_cars)
            deal_with_supplier(choice, autohouse)
