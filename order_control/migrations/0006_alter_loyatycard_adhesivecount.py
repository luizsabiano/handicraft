# Generated by Django 3.2.3 on 2021-06-29 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0005_auto_20210628_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loyatycard',
            name='adhesiveCount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
