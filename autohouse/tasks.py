from django.db import transaction
from django.db.models import F
from django.utils import timezone
from celery import shared_task

from autohouse.models import Autohouse, AutohouseCar
from main.models import Car
from supplier.models import SupplierCar, SupplierDiscount


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
        min_discount_price_list.append(min_discount_price)

        min_default_price = SupplierCar.objects.filter(
            car=car,
            is_active=True,
        ).order_by('price')[0]
        min_default_price_list.append(min_default_price)

    cheapest_discount_car = get_cheapest_car(min_discount_price_list)
    cheapest_default_car = get_cheapest_car(min_default_price_list)

    if cheapest_discount_car:
        if cheapest_discount_car.price < cheapest_default_car.price:
            return {
                'supplier': cheapest_discount_car.supplier,
                'price': cheapest_discount_car.price,
                'car': cheapest_discount_car.car
            }
    return {
        'supplier': cheapest_default_car.supplier,
        'price': cheapest_default_car.price,
        'car': cheapest_default_car.car
    }

    # if min_discount_price is not None:
    #     if min_discount_price.price < min_default_price.price:
    #         return {
    #             'supplier': min_discount_price.supplier_car.supplier,
    #             'price': min_discount_price.price,
    #             'car': min_discount_price.supplier_car.car
    #         }
    # return {
    #     'supplier': min_default_price.supplier,
    #     'price': min_default_price.price,
    #     'car': min_default_price.car
    # }


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
