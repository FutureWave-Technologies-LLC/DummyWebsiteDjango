# Generated by Django 5.1.2 on 2024-11-26 04:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_remove_replies_comment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='replies',
            name='comment',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='posts.comments'),
            preserve_default=False,
        ),
    ]
