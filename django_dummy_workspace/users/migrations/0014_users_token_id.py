# Generated by Django 5.1.2 on 2024-11-26 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_alter_users_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='token_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
