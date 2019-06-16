# Generated by Django 2.0.7 on 2019-06-16 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_s', models.DecimalField(decimal_places=2, default=8.0, max_digits=3)),
                ('water_s', models.DecimalField(decimal_places=2, default=8.0, max_digits=3)),
                ('play_s', models.DecimalField(decimal_places=2, default=8.0, max_digits=3)),
                ('happy_s', models.DecimalField(decimal_places=2, default=8.0, max_digits=3)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
        ),
    ]