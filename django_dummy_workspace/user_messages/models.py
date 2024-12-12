from django.db import models
from users.models import *
from random import randrange

def generate_message_id():
    while True:
        id = randrange(0, 9999999)
        if user_messages.objects.filter(message_id = id).count() == 0:
            break
    return id

from django.db import models
from users.models import users

class user_messages(models.Model):
    message_id = models.IntegerField(primary_key=True,
                                      null=False, 
                                      unique=True,
                                      default=generate_message_id)
    sender = models.ForeignKey(users, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_id = models.IntegerField()
    message_text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver_id}: {self.message_text}"
