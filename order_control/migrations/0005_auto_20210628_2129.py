# Generated by Django 3.2.3 on 2021-06-29 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0004_auto_20210626_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='loyatycard',
            name='adhesiveCount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='createAt',
            field=models.DateField(verbose_name='Pago em'),
        ),
    ]