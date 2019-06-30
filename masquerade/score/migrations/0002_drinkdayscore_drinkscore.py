# Generated by Django 2.0.7 on 2019-06-30 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
        ('score', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrinkDayScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=1, default=8.0, max_digits=2)),
                ('first_score', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('second_score', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('third_score', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
        ),
        migrations.CreateModel(
            name='DrinkScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=1, default=8.0, max_digits=2)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
        ),
    ]
