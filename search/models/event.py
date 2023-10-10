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
    invited_users = models.ManyToManyField(UserModel, through='EventInvitation')
    requests_to_join = models.ManyToManyField(UserModel,related_name="requested_events", blank=True)
    event_members = models.ManyToManyField(UserModel, related_name="events", blank=True)
    event_location = models.CharField(max_length=200)

    def clean(self) -> None:
        if self.start_date_time >= self.end_date_time:
            raise ValidationError(("Start date/time must be before End date/time"), code="invalid-date-time")
        
    def _add_uninvited_member(self, user:UserModel):
        #We know that user is not invited
        self.invited_users.through.objects.create(user= user, associated_event=self)
        self.save()
        return
        
    def add_members(self, adder:UserModel, user:UserModel):
        admin = self.religious_establishment.admins.all().filter(id = adder.id).exists()
        invited = self.invited_users.all().filter(id = adder.id).exists()
        if admin and not invited:
            self._add_uninvited_member(user)
        elif admin and invited:
            self.invited_users.remove(user)
            self.event_members.add(user)
            self.save()
        else:
            raise InvalidUserException()
        
    def __str__(self):
        return self.name