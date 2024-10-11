from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers

# Create your models here.

class likes(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    comment = models.CharField(max_length=45)
    like_count = models.IntegerField()

    def __str__(self):
        return self.name
    
class users(models.Model):                                         #Old model for user table, make sure to remove
    user_id = models.IntegerField(primary_key=True, null=False)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=45)
    status = models.BooleanField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    def __str__(self):
        return self.user_id

class personal_pages(models.Model):
    page_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.page_id

class posts(models.Model):
    post_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.post_id

class comments(models.Model):
    comment_id = models.IntegerField(primary_key=True, null=False)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.comment_id

class replies(models.Model):
    reply_id = models.IntegerField(primary_key=True, null=False)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.reply_id
    
class Chat(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"
    
class chat_participants(models.Model):
    chat = models.ForeignKey(Chat, related_name="participants", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="chat_participation", on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    #role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('member', 'Member')])

    def __str__(self):
        return f"{self.user.username} in Chat {self.chat.id}"

class messages(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username} in Chat {self.chat.id}"
    
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = messages  # Reference the 'messages' model here
        fields = ['message_id', 'chat', 'sender', 'receiver', 'text', 'timestamp']  # Include your desired fields