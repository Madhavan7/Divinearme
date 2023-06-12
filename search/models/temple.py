from django.db import models
from django.contrib.auth.models import User
from .location import location

class temple(models.Model):
    name = models.CharField(max_length=100)
    temple_location = models.OneToOneField(location, on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(User, through='temple_invitation', related_name="temple_invitations")
    requests_to_join = models.ManyToManyField(User, through='temple_request', related_name="temple_requests")
    temple_members = models.ManyToManyField(User, related_name="temples")
    #posts 
    def __str__(self):
        return self.name