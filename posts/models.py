from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class likes(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    comment = models.CharField(max_length=45)
    like_count = models.IntegerField()

    def __str__(self):
        return self.name

class posts(models.Model):
    post_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def str(self):
        return self.post_id

class comments(models.Model):
    comment_id = models.IntegerField(primary_key=True, null=False)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def str(self):
        return self.comment_id

class replies(models.Model):
    reply_id = models.IntegerField(primary_key=True, null=False)
    text = models.CharField(max_length=255)

    def str(self):
        return self.reply_id