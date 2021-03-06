# Generated by Django 3.2.3 on 2021-07-30 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0010_auto_20210710_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyatycard',
            name='isDelivered',
            field=models.BooleanField(default=False, verbose_name='Está entregue?'),
        ),
        migrations.AlterField(
            model_name='boxtop',
            name='type',
            field=models.CharField(choices=[('TOPO', 'TOPO DE BOLO'), ('CAIXA', 'CAIXA BOX'), ('Tag', 'Tag'), ('outros', 'Outros')], max_length=255),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='type',
            field=models.CharField(choices=[('PP', 'PicPay'), ('PIX', 'PIX'), ('CC', 'Cartão de Crédito'), ('CD', 'Cartão de Débito'), ('CASH', 'Dinheiro'), ('cc', 'Depósito')], max_length=255, verbose_name='Tipo'),
        ),
    ]
