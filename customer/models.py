from django.db import models

from authentication.models import CustomUser
from autohouse.schemas import EnumSchemas
from autohouse.validators import CharacteristicJSONValidationSchema
from main.models import CommonInfo, PurchaseHistory


class Customer(CommonInfo):
    user = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    preferred_car = models.JSONField(validators=[CharacteristicJSONValidationSchema(
        limit_value=EnumSchemas.CHARACTERISTIC_SCHEMA.value
    )], null=True)


class CustomerPurchaseHistory(PurchaseHistory):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
