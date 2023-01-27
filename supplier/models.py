from django.db import models

from main.models import CommonInfo, CommonCarInfo, CommonDiscount


class SupplierCar(CommonCarInfo):
    pass


class Supplier(CommonInfo):
    title = models.CharField(max_length=255)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)


class SupplierDiscount(CommonDiscount):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
