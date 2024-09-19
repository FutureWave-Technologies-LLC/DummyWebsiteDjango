from django.db import models

# Create your models here.

class client_info(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    age = models.CharField(max_length=45)

    def __str__(self):
        return self.name
    
class likes(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    comment = models.CharField(max_length=45)
    like_count = models.IntegerField()

    def __str__(self):
        return self.name