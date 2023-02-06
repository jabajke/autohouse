# Generated by Django 4.0 on 2023-02-06 09:30

import autohouse.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autohouse', '0004_remove_autohousediscount_autohouse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autohouse',
            name='prefer_characteristic',
            field=models.JSONField(null=True, validators=[autohouse.validators.CharacteristicJSONValidationSchema(limit_value={'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'body-type': {'type': 'string'}, 'brand': {'type': 'string'}, 'color': {'type': 'string'}, 'horse_power': {'minimum': 1, 'type': 'integer'}, 'model': {'type': 'string'}, 'transmission_type': {'type': 'string'}, 'year_of_issue': {'minimum': 1800, 'type': 'integer'}}, 'type': 'object'})]),
        ),
    ]