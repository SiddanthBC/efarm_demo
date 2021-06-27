from django.db import models

# Create your models here.

class PageView(models.Model):
    hostname = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

class creds(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length= 100)
    password = models.CharField(max_length=20)
