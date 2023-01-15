from datetime import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django_countries.fields import CountryField

from .validators import CharacteristicJSONValidationSchema
from .schemas import EnumSchemas


class CommonInfo(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Autohouse(CommonInfo):
    title = models.CharField(max_length=255)
    location = CountryField()
    prefer_characteristic = models.JSONField(validators=[CharacteristicJSONValidationSchema(
        limit_value=EnumSchemas.CHARACTERISTIC_SCHEMA.value
    )], null=True)

    def __str__(self):
        return self.title


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
        MinValueValidator(1800), MaxValueValidator(datetime.now().year)
    ], help_text="Use <YYYY> as date format")
    transmission_type = models.CharField(
        choices=TRANSMISSION_CHOICES, max_length=50
    )
    body_type = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(limit_value=1.00)])

    def __str__(self):
        return '{} | {}'.format(self.brand, self.model)
