# Generated by Django 3.2.3 on 2021-06-26 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0003_alter_client_createat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='createAt',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='createAt',
            field=models.DateField(),
        ),
    ]