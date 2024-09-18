from django.db import models

# Create your models here.

class client_info(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    age = models.IntegerField(max_length=45)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name