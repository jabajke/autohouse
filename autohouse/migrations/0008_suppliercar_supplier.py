# Generated by Django 4.1.5 on 2023-01-26 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autohouse', '0007_remove_suppliercar_autohouse'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliercar',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autohouse.supplier'),
        ),
    ]
