from django.db import models
from users.models import *
from random import randrange
import pytz

def convert_pst(time):
    if time.tzinfo is None:
        time = pytz.utc.localize(time)
    pst_timezone = pytz.timezone("America/Los_Angeles")
    return time.astimezone(pst_timezone)

class user_messages(models.Model):
    sender = models.ForeignKey(users, on_delete=models.CASCADE, default=None)

    message_id = models.AutoField(primary_key=True,
                                      null=False, 
                                      unique=True)
    receiver_id = models.IntegerField(null=False)
    message_text = models.CharField(max_length=255, null=False)

    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.message_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)
