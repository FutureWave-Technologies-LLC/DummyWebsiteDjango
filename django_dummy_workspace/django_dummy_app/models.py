from django.db import models

# Create your models here.

class dummy_table(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)

    def __string__(self):
        return self.title