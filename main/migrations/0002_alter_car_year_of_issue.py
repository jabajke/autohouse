# Generated by Django 4.0 on 2023-01-27 16:20

import django.core.validators
from django.db import migrations, models
import main.utils


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='year_of_issue',
            field=models.PositiveSmallIntegerField(help_text='Use <YYYY> as date format', validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(main.utils.Util.current_year)]),
        ),
    ]
