# Generated by Django 2.0.7 on 2019-06-16 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cat_breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=2)),
                ('zh_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='dog_breed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=2)),
                ('zh_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_id', models.IntegerField(unique=True)),
                ('nick_name', models.CharField(max_length=18, unique=True)),
                ('gender', models.IntegerField(default=1)),
                ('pet_type', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=5000)),
                ('ppp_status', models.IntegerField(default=0)),
                ('love_status', models.IntegerField(default=0)),
                ('birth_time', models.IntegerField(default=0)),
                ('breed_type', models.CharField(max_length=20)),
                ('food_weight', models.IntegerField(default=0)),
                ('activity', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.MasUser')),
            ],
        ),
    ]
