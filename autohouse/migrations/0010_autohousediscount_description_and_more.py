# Generated by Django 4.1.5 on 2023-01-26 12:54

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('autohouse', '0009_supplierdiscount_autohousediscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='autohousediscount',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='autohousediscount',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 12, 54, 41, 143802, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='autohousediscount',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='autohousediscount',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='supplierdiscount',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='supplierdiscount',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 12, 54, 41, 143802, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='supplierdiscount',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='supplierdiscount',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
