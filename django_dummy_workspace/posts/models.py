from django.db import models
from users.models import *
from random import randrange
# pip install pytz
import pytz

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
    
    post_id = models.AutoField(primary_key=True, 
                                  null=False,
                                  unique= True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.post_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)

class likes(models.Model):
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)

    like_id = models.AutoField(primary_key=True,
                                      null=False, 
                                      unique=True)

    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.like_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)
    
class comments(models.Model):
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)

    comment = models.CharField(max_length=256, null=False)

    comment_id = models.AutoField(primary_key=True,
                                      null=False, 
                                      unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.comment_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)

class replies(models.Model):
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    comment = models.ForeignKey(comments, on_delete=models.CASCADE)

    reply_id = models.AutoField(primary_key=True,
                                      null=False, 
                                      unique=True)

    reply = models.CharField(max_length=255, null=False)

    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.reply_id