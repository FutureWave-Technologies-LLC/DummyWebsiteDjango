from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class users(models.Model):                                         
    user_id = models.IntegerField(primary_key=True, null=False)
    username = models.CharField(max_length=15)
    password = models.CharField(max_length=45)
    status = models.BooleanField()
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    follower_id = models.IntegerField()

    def str(self):
        return self.user_id