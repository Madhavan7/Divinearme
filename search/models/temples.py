from django.db import models
from django.contrib.auth.models import User

class temple(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    members = models.ManyToManyField(User, through='membership')

    def __str__(self):
        return self.name