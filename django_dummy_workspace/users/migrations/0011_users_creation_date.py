# Generated by Django 5.1.2 on 2024-11-12 19:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_users_profile_image_alter_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
