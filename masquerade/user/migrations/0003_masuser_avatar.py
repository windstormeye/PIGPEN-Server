# Generated by Django 2.0.7 on 2018-10-03 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20181003_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='masuser',
            name='avatar',
            field=models.IntegerField(default=-1),
        ),
    ]