# Generated by Django 4.0 on 2023-01-27 12:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierdiscount',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 3, 12, 0, 9, 629667, tzinfo=utc)),
        ),
    ]
