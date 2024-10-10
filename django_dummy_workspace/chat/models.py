from django.db import models
from django_dummy_app.models import users  # The tutorial mentioned below uses the built-in DJango Users model, but for now I'll use the one we created.

# Create your models here.

# From this tutorial https://youtu.be/Q7N2oJTnThA?si=Nbhy02sBxpZk-g3r.
class Chat(models.Model):  # Model that stores all chats
    chat_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.group_name

class Message(models.Model):    # Stores messages from chats
    chat = models.ForeignKey(Chat, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(users, on_delete=models.CASCADE) 
    body = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.author.username} : {self.body}'