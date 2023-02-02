from celery import shared_task

from main.models import Car
from autohouse.models import Autohouse
from supplier.models import SupplierCar

@shared_task
def autohouse_buying():
    pass

