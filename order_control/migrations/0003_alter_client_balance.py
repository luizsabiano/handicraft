# Generated by Django 3.2.3 on 2021-06-03 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0002_auto_20210603_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
