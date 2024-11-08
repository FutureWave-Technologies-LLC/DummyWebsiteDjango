from django.db import models
from users.models import *
# pip install pytz
import pytz

def convert_pst(time):
    if time.tzinfo is None:
        time = pytz.utc.localize(time)
    pst_timezone = pytz.timezone("America/Los_Angeles")
    return time.astimezone(pst_timezone)

class posts(models.Model):
    user_model = models.ForeignKey(users, on_delete=models.CASCADE)
    
    post_id = models.IntegerField(primary_key=True, null=False)
    media = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.post_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)

class comments(models.Model):
    user_model = models.ForeignKey(users, on_delete=models.CASCADE)
    post_model = models.ForeignKey(posts, on_delete=models.CASCADE)

    comment_id = models.IntegerField(primary_key=True, null=False)
    user_id = models.IntegerField(null=False)
    post_id = models.IntegerField(null=False)
    comment = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.comment_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)

class replies(models.Model):
    reply_id = models.IntegerField(primary_key=True, null=False)
    user_id = models.IntegerField(null=False)
    comment_id = models.IntegerField(null=False)
    reply = models.CharField(max_length=255)

    def str(self):
        return self.reply_id