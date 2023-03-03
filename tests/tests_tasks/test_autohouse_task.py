import pytest

from autohouse.models import AutohouseCar, AutoHouseSupplierPurchaseHistory
from autohouse.tasks import autohouse_buying
from supplier.models import SupplierCar


@pytest.mark.django_db
def test_autohouse_buying_task(
        autohouse_fixture,
        supplier_fixture,
        supplier_car_fixture,
        car_fixture
):
    autohouse_buying()
    assert AutohouseCar.objects.filter(
        autohouse=autohouse_fixture,
        supplier=supplier_fixture,
        car=car_fixture,
    ).exists()


@pytest.mark.django_db
def test_autohouse_buying_task_discount_car(
        autohouse_fixture,
        supplier_fixture,
        supplier_discount_fixture,
        car_fixture
):
    autohouse_car = AutohouseCar.objects.filter(
        autohouse=autohouse_fixture,
        supplier=supplier_fixture,
        car=car_fixture
    )
    history = AutoHouseSupplierPurchaseHistory.objects.filter(
        autohouse=autohouse_fixture,
        supplier=supplier_fixture,
        car=car_fixture
    )
    assert history.exists() is False
    assert autohouse_car.exists() is False

    autohouse_buying()

    assert autohouse_car.exists()
    assert history.exists()

    supplier_car = SupplierCar.objects.get(
        supplier=supplier_fixture,
        car=car_fixture
    )
    assert supplier_car.price > history.first().price
