# Generated by Django 4.0.4 on 2022-06-15 16:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_movimientosbancarios_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientosbancarios',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2022, 6, 15, 13, 45, 0, 873843)),
        ),
        migrations.AlterField(
            model_name='movimientoserp',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2022, 6, 15, 13, 45, 0, 873843)),
        ),
        migrations.AlterField(
            model_name='saldosbancarios',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2022, 6, 15, 13, 45, 0, 871834)),
        ),
    ]
