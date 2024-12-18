# Generated by Django 5.1.2 on 2024-11-11 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_id', models.IntegerField(default=-1, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=45)),
                ('status', models.BooleanField()),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('follower_id', models.IntegerField()),
            ],
        ),
    ]
