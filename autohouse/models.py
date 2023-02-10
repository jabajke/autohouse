from django.core.validators import MinValueValidator
from django.db import models
from django_countries.fields import CountryField

from main.models import (CommonCarInfo, CommonDiscount, CommonInfo,
                         PurchaseHistory)
from supplier.models import Supplier

from .schemas import EnumSchemas
from .validators import CharacteristicJSONValidationSchema


class Autohouse(CommonInfo):
    title = models.CharField(max_length=255)
    location = CountryField()
    prefer_characteristic = models.JSONField(validators=[CharacteristicJSONValidationSchema(
        limit_value=EnumSchemas.CHARACTERISTIC_SCHEMA.value
    )], null=True)
    balance = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=10,
        validators=[MinValueValidator(limit_value=0.01)]
    )

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if 'horse_power' not in self.prefer_characteristic.keys():
            data = {'value': 1, 'actions': 'gte'}
            self.prefer_characteristic['horse_power'] = dict()
            self.prefer_characteristic['horse_power'].update(data)

        if 'year_of_issue' not in self.prefer_characteristic.keys():
            data = {'value': 1800, 'actions': 'gte'}
            self.prefer_characteristic['year_of_issue'] = dict()
            self.prefer_characteristic['year_of_issue'].update(data)
        super(Autohouse, self).save(**kwargs)


class AutohouseDiscount(CommonDiscount):
    autohouse_car = models.ForeignKey('AutohouseCar', on_delete=models.SET_NULL, null=True)


class AutohouseCar(CommonCarInfo):
    autohouse = models.ForeignKey(Autohouse, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveSmallIntegerField(default=1)


class AutoHouseSupplierPurchaseHistory(PurchaseHistory):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
