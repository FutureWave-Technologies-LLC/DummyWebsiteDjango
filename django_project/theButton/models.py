from django.db import models

# Create your models here.

class dummydata(models.Model):                      #VALUES (username, password)
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)