import pytest

from autohouse.services import AutohouseService

service = AutohouseService()


@pytest.mark.django_db
def test_autohouse_statistic(
        autohouse_purchase_history_fixture,
        autohouse_car_fixture,
        autohouse_fixture
):
    data = dict(
        best_partners='FooSupplier',
        most_expensive_car='FooCar',
    )
    service_keys = service.autohouse_statistic(autohouse_fixture).keys()
    test_keys = data.keys()
    assert service_keys == test_keys


@pytest.mark.django_db
def test_general_statistic_with_autohouse_car_and_history(
        customer_purchase_history_fixture,
        autohouse_car_fixture
):
    data = dict(
        average_price_of_cars=100.0,
        best_sellers='FooAutohouse',
        amount_of_customers=10,
        most_productive_autohouse='FooAutohouse'
    )
    service_keys = service.general_statistic().keys()
    test_keys = data.keys()
    assert service_keys == test_keys
