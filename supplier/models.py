from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from main.models import CommonCarInfo, CommonDiscount, CommonInfo
from main.utils import Util as main_util


class SupplierCar(CommonCarInfo):
    pass

    def __str__(self):
        return f'{self.car} | {self.supplier}'


class Supplier(CommonInfo):
    title = models.CharField(max_length=255)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    year_of_foundation = models.PositiveSmallIntegerField(default=1800, validators=[
        MinValueValidator(1800), MaxValueValidator(main_util.current_year)
    ], help_text="Use <YYYY> as date format")
    number_of_buyers = models.PositiveSmallIntegerField(default=0, validators=[
        MinValueValidator(0)])

    def __str__(self):
        return self.title


class SupplierDiscount(CommonDiscount):
    supplier_car = models.ForeignKey(SupplierCar, on_delete=models.SET_NULL, null=True)
