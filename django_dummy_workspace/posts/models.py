from django.db import models
from users.models import *
from random import randrange
# pip install pytz
import pytz

def generate_post_id():
    while True:
        id = randrange(0, 999999)
        if posts.objects.filter(post_id = id).count() == 0:
            break
    return id

def likes_id():
    while True:
        id = randrange(0, 999999)
        if likes.objects.filter(like_id = id).count() == 0:
            break
    return id

def generate_comments_id():
    while True:
        id = randrange(0, 999999)
        if comments.objects.filter(comment_id = id).count() == 0:
            break
    return id

def generate_replies_id():
    while True:
        id = randrange(0, 999999)
        if replies.objects.filter(reply_id = id).count() == 0:
            break
    return id

def convert_pst(time):
    if time.tzinfo is None:
        time = pytz.utc.localize(time)
    pst_timezone = pytz.timezone("America/Los_Angeles")
    return time.astimezone(pst_timezone)

class posts(models.Model):
    author = models.ForeignKey(users, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500, null=False)
    media = models.CharField(max_length=255, null=True)
    
    post_id = models.IntegerField(primary_key=True, 
                                  null=False,
                                  unique= True,
                                  default=generate_post_id)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.post_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)

class likes(models.Model):
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)

    like_id = models.IntegerField(primary_key=True,
                                      null=False, 
                                      unique=True,
                                      default=likes_id)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.like_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)
    
class comments(models.Model):
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)

    comment = models.CharField(max_length=256, null=False)

    comment_id = models.IntegerField(primary_key=True,
                                      null=False, 
                                      unique=True,
                                      default=generate_comments_id)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.comment_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)

class replies(models.Model):
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    comment = models.ForeignKey(comments, on_delete=models.CASCADE)

    reply_id = models.IntegerField(primary_key=True,
                                      null=False, 
                                      unique=True,
                                      default=generate_replies_id)

    reply = models.CharField(max_length=255, null=False)

    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.reply_id