from django.db import models
from django.forms import ValidationError
from .user_profile import UserModel
from .temple import temple
from search.exceptions.exceptions import InvalidUserException
class event(models.Model):
    religious_establishment = models.ForeignKey(temple, on_delete=models.CASCADE, related_name='events')
    private = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(UserModel, through='EventInvitation', related_name="event_invitations")
    requests_to_join = models.ManyToManyField(UserModel,related_name="requested_events", blank=True)
    event_members = models.ManyToManyField(UserModel, related_name="events", blank=True)
    event_location = models.CharField(max_length=200)

    def clean(self) -> None:
        if self.start_date_time >= self.end_date_time:
            raise ValidationError(("Start date/time must be before End date/time"), code="invalid-date-time")
        
    def add_members(self, adder:UserModel, user:UserModel):
        admin = self.religious_establishment.admins.all().filter(id = adder.id).exists()
        invited = self.invited_users.all().filter(id = adder.id).exists()
        #below the error is that queryset objects are not callable
        if admin or invited:
            if invited:
                self.invited_users.all().filter(user=user.id).delete()
            self.event_members.add(user)
            self.save()
            return True
        else:
            raise InvalidUserException()
    def __str__(self):
        return self.name