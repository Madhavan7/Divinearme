from django.db import models
from django.contrib.auth.models import User
from .user_profile import user_model
class temple(models.Model):
    name = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    temple_location = models.CharField(max_length = 200)
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(user_model, through='temple_invitation', related_name="temple_invitations")
    requests_to_join = models.ManyToManyField(user_model, related_name="temple_requests", blank=True)
    temple_members = models.ManyToManyField(user_model, related_name="temples", blank=True)
    admins = models.ManyToManyField(user_model, related_name="admins")
    #posts 
    def less_events(self):
        return self.events.all().order_by("-date")[:2]
    def less_members(self):
        return self.temple_members.all().order_by("username")[:5]
    #adds user to the admins, returns whether it was successful
    def add_admin(self, adder:user_model, user:user_model):
        if adder in self.admins.all():
            self.admins.add(user)
            self.save()
            return True
        return False
    #adds user to temple_members, returns whether the operation was a success
    def add_member(self, adder:user_model, user:user_model):
        if adder in self.admins.all():
            self.temple_members.add(user)
            self.save()
            return True
        return False
    def __str__(self):
        return self.name