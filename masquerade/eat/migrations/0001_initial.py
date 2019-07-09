# Generated by Django 2.0.7 on 2019-07-02 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foods', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='EatActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_foods', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('finished_time', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
        ),
    ]