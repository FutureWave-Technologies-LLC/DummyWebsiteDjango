import uuid
from django.db import models

def generate_user_id():
    return users.objects.all().count()+1

# Create your models here.
class users(models.Model):                                         
    user_id = models.IntegerField(primary_key=True, 
                                  unique=True, 
                                  null=False,
                                  editable=False,
                                  default=generate_user_id)
    
    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=150, null=False)
    profile_image = models.CharField(max_length=150)
    banner_image = models.CharField(max_length=150)
    profile_description = models.CharField(max_length=255)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    token_id = models.IntegerField(null=False)

    creation_date = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return self.user_id
