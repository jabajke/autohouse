# Generated by Django 4.0 on 2023-01-15 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autohouse', '0004_car_model_alter_autohouse_prefer_characteristic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='transmission_type',
            field=models.CharField(choices=[('manual', 'manual'), ('automatic', 'automatic'), ('cvt', 'cvt')], max_length=50),
        ),
    ]
