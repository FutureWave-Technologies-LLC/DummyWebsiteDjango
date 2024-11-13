# Generated by Django 5.1.2 on 2024-11-11 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_posts_user_model'),
        ('users', '0009_alter_users_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='user_model',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='posts',
            old_name='user_model',
            new_name='author',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='text',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='username',
        ),
        migrations.RemoveField(
            model_name='replies',
            name='user_id',
        ),
        migrations.AddField(
            model_name='posts',
            name='description',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='replies',
            name='author',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='users.users'),
            preserve_default=False,
        ),
    ]
