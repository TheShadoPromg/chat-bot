# Generated by Django 4.0.3 on 2022-03-29 14:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='numero',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Numero'),
        ),
        migrations.AlterField(
            model_name='gasto',
            name='fecha',
            field=models.DateField(default=datetime.date(2022, 3, 29), verbose_name='Fecha'),
        ),
    ]