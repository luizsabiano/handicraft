# Generated by Django 3.2.3 on 2021-07-03 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0007_boxtop_gift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boxtop',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Valor total das Caixas R$'),
        ),
    ]