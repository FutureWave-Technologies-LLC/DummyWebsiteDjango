# Generated by Django 5.1.2 on 2024-11-11 21:43

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_users_follower_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='first_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='users',
            name='last_name',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=20),
        ),
        # migrations.AlterField(
        #     model_name='users',
        #     name='user_id',
        #     field=models.IntegerField(default=users.models.generate_user_id, primary_key=True, serialize=False, unique=True),
        # ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=20),
        ),
    ]
