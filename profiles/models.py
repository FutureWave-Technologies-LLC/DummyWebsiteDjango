from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class personal_pages(models.Model):
    page_id = models.IntegerField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def str(self):
        return self.page_id

class follow(models.Model):
    primary_key = models.IntegerField(primary_key=True, null = False)
    follower_id = models.IntegerField(null=False)
    followee_id = models.IntegerField(null=False)

    def str(self):
        return self.follow_id