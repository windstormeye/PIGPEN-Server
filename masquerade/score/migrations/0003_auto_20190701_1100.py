# Generated by Django 2.0.7 on 2019-07-01 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score', '0002_drinkdayscore_drinkscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drinkdayscore',
            name='first_score',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='drinkdayscore',
            name='score',
            field=models.DecimalField(decimal_places=1, default=8.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='drinkdayscore',
            name='second_score',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='drinkdayscore',
            name='third_score',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=3),
        ),
    ]
