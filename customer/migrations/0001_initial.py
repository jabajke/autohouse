# Generated by Django 4.0 on 2023-01-30 21:51

import autohouse.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0002_alter_car_year_of_issue'),
        ('authentication', '0002_alter_customuser_groups_and_more'),
        ('autohouse', '0003_autohousecar_amount_autohousesupplierpurchasehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('preferred_car', models.JSONField(null=True, validators=[autohouse.validators.CharacteristicJSONValidationSchema(limit_value={'$schema': 'http://json-schema.org/draft-04/schema#', 'properties': {'body-type': {'type': 'string'}, 'brand': {'type': 'string'}, 'color': {'type': 'string'}, 'horse_power': {'minimum': 1, 'type': 'integer'}, 'model': {'type': 'string'}, 'price': {'type': 'number'}, 'transmission_type': {'type': 'string'}, 'year_of_issue': {'minimum': 1800, 'type': 'integer'}}, 'type': 'object'})])),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.customuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerPurchaseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(limit_value=1.0)])),
                ('amount', models.PositiveSmallIntegerField(default=1)),
                ('autohouse', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autohouse.autohouse')),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.car')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
