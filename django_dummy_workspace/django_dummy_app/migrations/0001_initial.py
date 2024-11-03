# Generated by Django 5.1.1 on 2024-11-03 20:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='follow',
            fields=[
                ('primary_key', models.IntegerField(primary_key=True, serialize=False)),
                ('follower_id', models.IntegerField()),
                ('followee_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='likes',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45)),
                ('comment', models.CharField(max_length=45)),
                ('like_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='replies',
            fields=[
                ('reply_id', models.IntegerField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=45)),
                ('status', models.BooleanField()),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('follower_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='messages',
            fields=[
                ('message_id', models.IntegerField(primary_key=True, serialize=False)),
                ('reciever_id', models.IntegerField()),
                ('text', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='personal_pages',
            fields=[
                ('page_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='posts',
            fields=[
                ('post_id', models.IntegerField(primary_key=True, serialize=False)),
                ('media', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dummy_app.posts')),
            ],
        ),
    ]
