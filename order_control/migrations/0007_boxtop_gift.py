# Generated by Django 3.2.3 on 2021-07-03 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0006_alter_loyatycard_adhesivecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='boxtop',
            name='gift',
            field=models.BooleanField(default=False, verbose_name='Brinde?'),
        ),
    ]
