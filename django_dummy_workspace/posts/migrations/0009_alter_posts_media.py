# Generated by Django 5.1.2 on 2024-11-11 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_posts_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='media',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
