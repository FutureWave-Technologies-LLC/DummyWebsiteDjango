from django.db import models
from users.models import users
from random import randrange

# Create your models here.
class follow(models.Model):
    follower = models.ForeignKey(users, on_delete=models.CASCADE)
    
    pk_follow = models.AutoField(primary_key=True, 
                                      null = False,
                                      unique= True)
    followee_id = models.IntegerField(null=False)

    def str(self):
        return self.followee_id