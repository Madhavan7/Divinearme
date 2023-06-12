from django.db import models
from django.contrib.auth.models import User

from .temple import temple
from .location import location

class event(models.Model):
    religious_establishment = models.ForeignKey(temple, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(User, through='event_invitation', related_name="event_invitations")
    requests_to_join = models.ManyToManyField(User, through='event_request', related_name="requested_events")
    event_members = models.ManyToManyField(User, related_name="events")
    event_location = models.OneToOneField(location, on_delete=models.CASCADE, null=True)
    # Additional fields for the event

    def __str__(self):
        return self.name