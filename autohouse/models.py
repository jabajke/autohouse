from django.db import models
from django_countries.fields import CountryField

from main.models import (
    CommonCarInfo,
    CommonDiscount,
    CommonInfo,
    PurchaseHistory
)
from supplier.models import Supplier

from .schemas import EnumSchemas
from .validators import CharacteristicJSONValidationSchema


class Autohouse(CommonInfo):
    title = models.CharField(max_length=255)
    location = CountryField()
    prefer_characteristic = models.JSONField(validators=[CharacteristicJSONValidationSchema(
        limit_value=EnumSchemas.CHARACTERISTIC_SCHEMA.value
    )], null=True)

    def __str__(self):
        return self.title


class AutohouseDiscount(CommonDiscount):
    autohouse = models.ForeignKey(Autohouse, on_delete=models.SET_NULL, null=True)


class AutohouseCar(CommonCarInfo):
    autohouse = models.ForeignKey(Autohouse, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveSmallIntegerField(default=1)


class AutoHouseSupplierPurchaseHistory(PurchaseHistory):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
