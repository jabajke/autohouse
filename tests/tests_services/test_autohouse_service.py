import pytest

from autohouse.services import AutohouseService

service = AutohouseService()


@pytest.mark.django_db
def test_autohouse_statistic(
        autohouse_purchase_history_fixture,
        autohouse_car_fixture,
        autohouse_fixture
):
    assert service.autohouse_statistic(autohouse_fixture)


@pytest.mark.django_db
def test_general_statistic(
        customer_purchase_history_fixture,
        autohouse_car_fixture
):
    assert service.general_statistic()
