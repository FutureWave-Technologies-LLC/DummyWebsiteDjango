from django.db import models
from django.contrib.auth.models import User
# pip install pytz
import pytz
import uuid

# Create your models here.

def generate_message_id():
    while True:
        id = uuid.uuid4()
        if user_messages.objects.filter(message_id=id).count() == 0:
            break
    return id

def convert_pst(time):
    if time.tzinfo is None:
        time = pytz.utc.localize(time)
    pst_timezone = pytz.timezone("America/Los_Angeles")
    return time.astimezone(pst_timezone)


class likes(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    comment = models.CharField(max_length=45)
    like_count = models.IntegerField()

    def __str__(self):
        return self.name
    
# class users(models.Model):                                         
#     user_id = models.IntegerField(primary_key=True, unique=True, null=False)
#     username = models.CharField(max_length=15)
#     password = models.CharField(max_length=45)
#     status = models.BooleanField()
#     first_name = models.CharField(max_length=45)
#     last_name = models.CharField(max_length=45)
#     follower_id = models.IntegerField()

#     def str(self):
#         return self.user_id

class personal_pages(models.Model):
    page_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
        return self.page_id

class posts(models.Model):
    post_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    comment_id = models.IntegerField(primary_key=True, null=False)
    user_id = models.IntegerField(null=False)
    post_id = models.IntegerField(null=False)
    comment = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    # post = models.ForeignKey(posts, on_delete=models.CASCADE)

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

class user_messages(models.Model):
    message_id = models.IntegerField(primary_key=True, default=generate_message_id, unique=True, null=False)
    user_id = models.IntegerField(null=False)
    reciever_id = models.IntegerField(null=False)
    text = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.message_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)
    
class follow(models.Model):
    primary_key = models.IntegerField(primary_key=True, null = False)
    follower_id = models.IntegerField(null=False)
    followee_id = models.IntegerField(null=False)

    def str(self):
        return self.follow_id