import pytest

from customer.services import CustomerService

service = CustomerService()


@pytest.mark.django_db
def test_get_active_customer_offers(correct_user_fixture, customer_fixture):
    assert service.get_customer(correct_user_fixture.pk) == customer_fixture


@pytest.mark.django_db
def test_check_car_exists(customer_fixture, customer_purchase_history_fixture):
    assert service.check_car_exists(customer_fixture) is True


@pytest.mark.django_db
def test_own_statistic(
        offer_fixture,
        customer_purchase_history_fixture,
        customer_fixture
):
    data = dict(
        offers_count=1,
        car_bought=1,
        money_spent=100,
        lovely_brand='FooBrand',
    )
    service_keys = service.own_statistic(customer_fixture).keys()
    test_keys = data.keys()
    assert service_keys == test_keys
