# Generated by Django 2.0.7 on 2018-07-31 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='reply_to',
        ),
        migrations.AlterField(
            model_name='comment',
            name='masuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.MasUser'),
        ),
    ]
