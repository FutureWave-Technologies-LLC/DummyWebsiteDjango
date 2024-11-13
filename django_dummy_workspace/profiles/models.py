from django.db import models
from users.models import users
from random import randrange

def generate_follow_pk():
    while True:
        id = randrange(0, 999999)
        if follow.objects.filter(pk_follow = id).count() == 0:
            break
    return id

# Create your models here.
class follow(models.Model):
    follower = models.ForeignKey(users, on_delete=models.CASCADE)
    
    pk_follow = models.IntegerField(primary_key=True, 
                                      null = False,
                                      unique= True,
                                      default=generate_follow_pk)
    followee_id = models.IntegerField(null=False)

    def str(self):
        return self.followee_id