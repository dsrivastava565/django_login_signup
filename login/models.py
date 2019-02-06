from django.db import models


class User(models.Model):
    username = models.CharField(max_length=1000)
    password = models.CharField(max_length=500)
    token = models.CharField(max_length=1000)
