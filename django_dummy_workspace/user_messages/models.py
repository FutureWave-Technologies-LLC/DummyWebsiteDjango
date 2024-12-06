'''
from django.db import models
from users.models import *
from random import randrange
import pytz

def generate_message_id():
    while True:
        id = randrange(0, 9999999)
        if user_messages.objects.filter(message_id = id).count() == 0:
            break
    return id

def convert_pst(time):
    if time.tzinfo is None:
        time = pytz.utc.localize(time)
    pst_timezone = pytz.timezone("America/Los_Angeles")
    return time.astimezone(pst_timezone)

class user_messages(models.Model):
    sender = models.ForeignKey(users, on_delete=models.CASCADE, default=None)

    message_id = models.IntegerField(primary_key=True,
                                      null=False, 
                                      unique=True,
                                      default=generate_message_id)
    receiver_id = models.IntegerField(null=False)
    message_text = models.CharField(max_length=255, null=False)

    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.message_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)
'''

from django.db import models
from users.models import users

class user_messages(models.Model):
    sender = models.ForeignKey(users, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_id = models.IntegerField()
    message_text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver_id}: {self.message_text}"
