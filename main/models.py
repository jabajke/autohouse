from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .utils import Util as main_util


class CommonInfo(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class CommonCarInfo(CommonInfo):
    car = models.ForeignKey('main.Car', on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(limit_value=1.00)])

    class Meta:
        abstract = True


class CommonDiscount(CommonInfo):
    car = models.ForeignKey('main.Car', on_delete=models.SET_NULL, null=True)
    discount = models.DecimalField(
        default=0, decimal_places=2, max_digits=5,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(100.00)
        ]
    )
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=main_util.default_end_date)

    class Meta:
        abstract = True


class Car(CommonInfo):
    TRANSMISSION_CHOICES = [
        ('manual', 'manual'),
        ('automatic', 'automatic'),
        ('cvt', 'cvt')
    ]
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    horse_power = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=50)
    year_of_issue = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1800), MaxValueValidator(main_util.current_year)
    ], help_text="Use <YYYY> as date format")
    transmission_type = models.CharField(
        choices=TRANSMISSION_CHOICES, max_length=50
    )
    body_type = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(limit_value=1.00)])

    def __str__(self):
        return '{} | {}'.format(self.brand, self.model)
