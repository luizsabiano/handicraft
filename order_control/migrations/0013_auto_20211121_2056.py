# Generated by Django 3.2.3 on 2021-11-21 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_control', '0012_auto_20211121_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AddField(
            model_name='client',
            name='password',
            field=models.CharField(default=True, max_length=50, verbose_name='Senha'),
            preserve_default=False,
        ),
    ]
