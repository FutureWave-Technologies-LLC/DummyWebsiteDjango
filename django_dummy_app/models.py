from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class messages(models.Model):
    message_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reciever_id = models.IntegerField(null=False)
    text = models.CharField(max_length=255)

    def str(self):
        return self.message_id