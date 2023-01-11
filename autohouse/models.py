from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField

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
    prefer_characteristic = models.ManyToManyField('Characteristic')

class Car(CommonInfo):
    characteristic = models.ForeignKey('Characteristic', on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10,
                                validators=[MinValueValidator(limit_value=1.00)])

class Characteristic(CommonInfo):
    title = models.JSONField(validators=[CharacteristicJSONValidationSchema(
        limit_value=EnumSchemas.CHARACTERISTIC_SCHEMA.value
    )])

    def __str__(self):
        return self.title['brand']
