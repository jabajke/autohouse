import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from customer.models import Customer, Offer

User = get_user_model()


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
