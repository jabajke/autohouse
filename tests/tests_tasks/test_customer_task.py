import pytest

from autohouse.models import AutohouseCar
from customer.models import Offer
from customer.tasks import offer_task


@pytest.mark.django_db
def test_customer_offer_task(
        autohouse_fixture,
        car_fixture,
        customer_fixture,
        prefer_car_correct_fixture,
        autohouse_car_fixture,
):
    offer = Offer.objects.create(
        customer=customer_fixture,
        preferred_car=prefer_car_correct_fixture,
        price=100
    )
    offer_task()
    offer.refresh_from_db()
    assert offer.is_active is False
    assert offer.is_completed


@pytest.mark.django_db
def test_customer_offer_task_discount_car(
        autohouse_fixture,
        car_fixture,
        customer_fixture,
        prefer_car_correct_fixture,
        autohouse_discount_fixture
):
    offer = Offer.objects.create(
        customer=customer_fixture,
        preferred_car=prefer_car_correct_fixture,
        price=100
    )
    offer_task()
    offer.refresh_from_db()
    autohouse_car = AutohouseCar.objects.get(autohouse=autohouse_fixture)
    assert offer.price < autohouse_car.price
