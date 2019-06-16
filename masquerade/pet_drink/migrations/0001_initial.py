# Generated by Django 2.0.7 on 2019-06-16 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetDrink',
            fields=[
                ('pet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pet.Pet')),
                ('water_consume', models.IntegerField(default=100)),
                ('water_residue', models.IntegerField(default=0)),
                ('water_consume_min', models.DecimalField(decimal_places=2, max_digits=4)),
                ('add_water_time', models.IntegerField()),
                ('finish_time', models.IntegerField()),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PetDrinkLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_water', models.IntegerField(default=0)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-updated_time'],
            },
        ),
        migrations.CreateModel(
            name='PetDrinkMarks',
            fields=[
                ('pet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pet.Pet')),
                ('water_marks', models.DecimalField(decimal_places=2, default=10, max_digits=4)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PetDrinkWaterDayMarks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_marks', models.DecimalField(decimal_places=2, default=10, max_digits=4)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PetDrinkWaterHourMarks',
            fields=[
                ('pet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pet.Pet')),
                ('water_8_marks', models.DecimalField(decimal_places=2, max_digits=4)),
                ('water_16_marks', models.DecimalField(decimal_places=2, max_digits=4)),
                ('water_24_marks', models.DecimalField(decimal_places=2, max_digits=4)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='petdrinkwaterdaymarks',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet'),
        ),
        migrations.AddField(
            model_name='petdrinklog',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet'),
        ),
    ]
