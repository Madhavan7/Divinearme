from django.db import models
from .user_profile import UserModel
from .temple import temple

class event(models.Model):
    religious_establishment = models.ForeignKey(temple, on_delete=models.CASCADE, related_name='events')
    private = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(UserModel, through='EventInvitation', related_name="event_invitations")
    requests_to_join = models.ManyToManyField(UserModel,related_name="requested_events", blank=True)
    event_members = models.ManyToManyField(UserModel, related_name="events", blank=True)
    event_location = models.CharField(max_length=200)
    # Additional fields for the event
    def less_members(self):
        return self.event_members.all().order_by("username")[:5]
    def less_posts(self):
        return self.posts.all().order_by("-date_added")[:3]
    def __str__(self):
        return self.name