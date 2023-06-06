from django.db import models
from django.contrib.auth.models import User
from Divinearme.search.models.location import location

class temple(models.Model):
    name = models.CharField(max_length=100)
    location = models.ManyToOneRel(location)
    members = models.ManyToManyField(User, through='membership')

    def __str__(self):
        return self.name