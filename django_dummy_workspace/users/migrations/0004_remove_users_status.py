# Generated by Django 5.1.2 on 2024-11-11 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_users_first_name_alter_users_last_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='status',
        ),
    ]
