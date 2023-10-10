from django.db import models
from .user_profile import UserModel
from search.exceptions.exceptions import InvalidUserException
class temple(models.Model):
    name = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    temple_location = models.CharField(max_length = 200)
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(UserModel, through='TempleInvitation')
    requests_to_join = models.ManyToManyField(UserModel, related_name="temple_requests", blank=True)
    temple_members = models.ManyToManyField(UserModel, related_name="temples", blank=True)
    admins = models.ManyToManyField(UserModel, related_name="admins")
    #posts 
    def less_events(self):
        return self.events.all().order_by("-date")[:2]
    def less_members(self):
        return self.temple_members.all().order_by("username")[:5]
    
    def _add_uninvited_member(self, user:UserModel, name:str):
        #at this point we know that user is not invited
        member = self.temple_members.all().filter(id = user.id).exists()
        if not member and name != "temple_members":
            raise InvalidUserException()
        elif not member and name == "temple_members":
            #problem here since invited_users is a multi-table model, need a TempleInvitation first
            self.invited_users.through.objects.create(user= user, associated_temple=self)
            self.save()
            return
        elif name != "temple_members":
            getattr(self, name).add(user)
            self.save()
            return


    #adds user to temple_members, returns whether the operation was a success
    def add_member(self, adder:UserModel, user:UserModel, name:str):
        #I need to edit below because too many if statements is not a god idea
        admin = self.admins.all().filter(id = adder.id).exists()
        invited = self.invited_users.all().filter(id = user.id).exists()
        if name == "admins" and not admin:
            raise InvalidUserException()
        if admin or invited:
            if invited:
                self.invited_users.remove(user.id)
                if name == "temple_members":
                    self.temple_members.add(user)
                    self.save()
            #must be admin and not invited
            else:
                self._add_uninvited_member(user, name)
            return True
        else:
            raise InvalidUserException()

    def remove_member(self, remover: UserModel, user:UserModel):
        admin = self.admins.all().filter(id = remover.id).exists()
        member_is_admin = self.admins.all().filter(id = user.id).exists()
        member = self.temple_members.all().filter(id=user.id).exists()
        if not admin or member_is_admin:
            raise InvalidUserException()
        elif member:
            self.temple_members.remove(user)
        else:
            return

    def add_event(self, adder:UserModel, event):
        admin = self.admins.all().filter(id = adder.id).exists()
        if admin:
            getattr(self, "events").add(event)
            self.save()
            return True
        else:
            raise InvalidUserException()
    
    def remove_event(self, remover:UserModel, event):
        admin = self.admins.all().filter(id=remover.id).exists()
        if admin and self.events.all().filter(id=event.id).exists():
            event.delete()
        else:
            raise InvalidUserException()
        self.save()
    def __str__(self):
        return self.name