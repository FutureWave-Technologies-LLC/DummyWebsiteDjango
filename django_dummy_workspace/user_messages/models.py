from django.db import models
from users.models import *
import pytz
import uuid

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

class user_messages(models.Model):
    user_model = models.ForeignKey(users, on_delete=models.CASCADE, default=None)
    user_id = models.IntegerField(null=False)

    message_id = models.IntegerField(primary_key=True, default=generate_message_id, unique=True, null=False)
    reciever_id = models.IntegerField(null=False)
    text = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.message_id
    def pst_creation_date(self):
        return convert_pst(self.creation_date)
