import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from autohouse.models import (Autohouse, AutohouseCar, AutohouseDiscount,
                              AutoHouseSupplierPurchaseHistory)
from customer.models import Customer, CustomerPurchaseHistory, Offer
from main.models import Car
from supplier.models import Supplier, SupplierCar, SupplierDiscount

User = get_user_model()

pytest_plugins = ('celery.contrib.pytest',)


@pytest.fixture
def payload_fixture():
    payload = dict(
        first_name='Foo',
        last_name='Bar',
        email='foo@bar.com',
        password='foobarpassword',
    )
    return payload


@pytest.fixture
def correct_user_fixture(payload_fixture):
    user = User.objects.create_user(**payload_fixture)
    user.is_active = True
    user.save()
    return user


@pytest.fixture
def wrong_user_fixture(payload_fixture):
    user = User.objects.create_user(**payload_fixture)
    return user


@pytest.fixture
def customer_fixture(correct_user_fixture):
    customer, created = Customer.objects.get_or_create(user=correct_user_fixture)
    customer.balance = 10000
    customer.save()
    return customer


@pytest.fixture
def logged_in_user(correct_user_fixture):
    refresh = RefreshToken.for_user(correct_user_fixture)
    access = refresh.access_token
    return {'access': str(access), 'refresh': str(refresh)}


@pytest.fixture
def prefer_car_correct_fixture():
    payload = dict(
        brand="foo",
        model="bar",
        horse_power={"value": 100, "actions": "gte"},
        color=["black", "green"],
        year_of_issue={"value": 2010, "actions": "gte"},
        transmission_type="manual",
        body_type="pickup"
    )
    return payload


@pytest.fixture
def offer_fixture(customer_fixture, prefer_car_correct_fixture):
    offer = Offer.objects.create(
        customer=customer_fixture,
        preferred_car=prefer_car_correct_fixture,
        price=100
    )
    return offer


@pytest.fixture
def customer_purchase_history_fixture(customer_fixture):
    history = CustomerPurchaseHistory.objects.create(customer=customer_fixture, price=10)
    return history


@pytest.fixture
def car_fixture(prefer_car_correct_fixture):
    horse_power = prefer_car_correct_fixture.pop('horse_power').get('value')
    year_of_issue = prefer_car_correct_fixture.pop('year_of_issue').get('value')
    color = prefer_car_correct_fixture.pop('color')[0]
    car = Car.objects.create(
        **prefer_car_correct_fixture,
        horse_power=horse_power,
        year_of_issue=year_of_issue,
        color=color
    )
    return car


@pytest.fixture
def supplier_fixture():
    supplier = Supplier.objects.create(
        title='FooSupplierTitle',
        balance=1000.00,
        year_of_foundation=2010
    )
    return supplier


@pytest.fixture
def autohouse_fixture(prefer_car_correct_fixture):
    autohouse = Autohouse.objects.create(
        title='FooTitleAutohouse',
        location='AF',
        prefer_characteristic=prefer_car_correct_fixture,
        balance=100000.0,
    )
    return autohouse


@pytest.fixture
def autohouse_car_fixture(
        autohouse_fixture,
        car_fixture,
        supplier_fixture
):
    autohouse_car = AutohouseCar.objects.create(
        autohouse=autohouse_fixture,
        car=car_fixture,
        supplier=supplier_fixture,
        price=100.0
    )
    return autohouse_car


@pytest.fixture
def autohouse_purchase_history_fixture(
        autohouse_fixture,
        supplier_fixture,
        car_fixture
):
    history = AutoHouseSupplierPurchaseHistory.objects.create(
        autohouse=autohouse_fixture,
        supplier=supplier_fixture,
        car=car_fixture,
        price=100.0
    )
    return history


@pytest.fixture
def supplier_car_fixture(car_fixture, supplier_fixture):
    supplier_car = SupplierCar.objects.create(
        supplier=supplier_fixture,
        car=car_fixture,
        price=100.00
    )
    return supplier_car


@pytest.fixture
def supplier_discount_fixture(supplier_car_fixture, supplier_fixture):
    discount = SupplierDiscount.objects.create(
        supplier_car=supplier_car_fixture,
        title='FooTitleDiscount',
        discount=99.00
    )
    return discount


@pytest.fixture
def autohouse_discount_fixture(
        autohouse_car_fixture
):
    discount = AutohouseDiscount.objects.create(
        autohouse_car=autohouse_car_fixture,
        discount=99
    )
    return discount
