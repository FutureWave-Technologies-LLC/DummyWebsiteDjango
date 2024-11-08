from django.db import models
from users.models import users

# Create your models here.
class follow(models.Model):
    followee_model = models.ForeignKey(users, on_delete=models.CASCADE)
    
    primary_key = models.IntegerField(primary_key=True, null = False)
    follower_id = models.IntegerField(null=False)
    followee_id = models.IntegerField(null=False)

    def str(self):
        return self.follow_id