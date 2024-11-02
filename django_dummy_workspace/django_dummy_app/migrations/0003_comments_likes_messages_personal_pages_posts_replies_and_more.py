# Generated by Django 5.1.1 on 2024-09-27 00:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_dummy_app', '0002_alter_dummy_table_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='comments',
            fields=[
                ('comment_id', models.IntegerField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=255)),
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
            name='messages',
            fields=[
                ('message_id', models.IntegerField(primary_key=True, serialize=False)),
                ('reciever_id', models.IntegerField()),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='personal_pages',
            fields=[
                ('page_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='posts',
            fields=[
                ('post_id', models.IntegerField(primary_key=True, serialize=False)),
                ('media', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255)),
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
            ],
        ),
        migrations.DeleteModel(
            name='dummy_table',
        ),
        migrations.AddField(
            model_name='comments',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dummy_app.posts'),
        ),
        migrations.AddField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dummy_app.users'),
        ),
        migrations.AddField(
            model_name='personal_pages',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dummy_app.users'),
        ),
        migrations.AddField(
            model_name='messages',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_dummy_app.users'),
        ),
    ]