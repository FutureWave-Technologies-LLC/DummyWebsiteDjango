# Generated by Django 5.1.2 on 2024-11-12 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_users_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=150),
        ),
    ]
