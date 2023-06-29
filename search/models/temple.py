from django.db import models
from django.contrib.auth.models import User

class temple(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    temple_location = models.CharField(max_length = 200)
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(User, through='temple_invitation', related_name="temple_invitations")
    requests_to_join = models.ManyToManyField(User, related_name="temple_requests", blank=True)
    temple_members = models.ManyToManyField(User, related_name="temples", blank=True)
    #posts 
    def less_events(self):
        return self.events.all().order_by("-date")[:2]
    def less_members(self):
        return self.temple_members.all().order_by("username")[:5]
    def __str__(self):
        return self.name