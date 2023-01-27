# Generated by Django 4.0 on 2023-01-27 11:40

import autohouse.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autohouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('location', django_countries.fields.CountryField(max_length=2)),
                ('prefer_characteristic', models.JSONField(null=True, validators=[autohouse.validators.CharacteristicJSONValidationSchema(limit_value={'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'body-type': {'type': 'string'}, 'brand': {'type': 'string'}, 'color': {'type': 'string'}, 'horse_power': {'minimum': 1, 'type': 'integer'}, 'model': {'type': 'string'}, 'price': {'type': 'number'}, 'transmission_type': {'type': 'string'}, 'year_of_issue': {'minimum': 1800, 'type': 'integer'}}, 'type': 'object'})])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
