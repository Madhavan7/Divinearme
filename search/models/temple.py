from django.db import models
from django.contrib.auth.models import User
from .user_profile import UserModel
from search.exceptions.exceptions import InvalidUserException
class temple(models.Model):
    name = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    temple_location = models.CharField(max_length = 200)
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(UserModel, through='TempleInvitation', related_name="temple_invitations")
    requests_to_join = models.ManyToManyField(UserModel, related_name="temple_requests", blank=True)
    temple_members = models.ManyToManyField(UserModel, related_name="temples", blank=True)
    admins = models.ManyToManyField(UserModel, related_name="admins")
    #posts 
    def less_events(self):
        return self.events.all().order_by("-date")[:2]
    def less_members(self):
        return self.temple_members.all().order_by("username")[:5]
    #adds user to the admins, returns whether it was successful
    def add_admin(self, adder:UserModel, user:UserModel):
        if adder in self.admins.all():
            self.admins.add(user)
            self.save()
            return True
        return False
    #adds user to temple_members, returns whether the operation was a success
    def add_member(self, adder:UserModel, user:UserModel, name:str):
        print("adding")
        admins = self.admins.all()
        invited = self.invited_users.all()
        if name == "admins" and adder not in admins:
            raise InvalidUserException()
        #below the error is that queryset objects are not callable
        if admins.filter(id = adder.id).exists() or user in invited:
            print("hello")
            print(name, user)
            getattr(self, name).add(user)
            self.save()
            return True
        else:
            raise InvalidUserException()
    def __str__(self):
        return self.name