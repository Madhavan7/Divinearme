from django.db import models
from django.contrib.auth.models import User
from Divinearme.search.models.location import location

class temple(models.Model):
    name = models.CharField(max_length=100)
    temple_location = models.ManyToOneRel(location)
    invited_users = models.ManyToManyField(User, through='temple_invitation')
    requests_to_join = models.ManyToManyField(User, through='temple_invitation')
    temple_members = models.ManyToManyField(User)
    def __str__(self):
        return self.name