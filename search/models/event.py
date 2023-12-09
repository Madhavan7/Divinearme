from django.db import models
from django.forms import ValidationError
from .user_profile import UserModel
from .temple import temple
from search.exceptions.exceptions import InvalidUserException
import googlemaps as gmaps
import googlemaps.places as places
import googlemaps.addressvalidation as addval
import search.apikeys as apikeys

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
    #Location based parameters
    event_location = models.CharField(max_length=200)
    placeID = models.CharField(max_length = 200)
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    lattitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    class Meta:
        ordering = ["start_date_time"]

    def clean(self) -> None:
        client = gmaps.Client(key=apikeys.GOOGLE_PLACES_API_KEY)
        response = addval.addressvalidation(client=client, addressLines=[getattr(self,'event_location')])
        for component in response['result']['address']['addressComponents']:
            if component['confirmationLevel'] != 'CONFIRMED':
                raise ValidationError("incorrect component " + component['componentType'] + ": " + component['confirmationLevel'], code="incorrect-component")
        if self.start_date_time >= self.end_date_time:
            raise ValidationError(("Start date/time must be before End date/time"), code="invalid-date-time")
    
    def save(self, *args, **kwargs):
        location = self.religious_establishment.temple_location if self.event_location == '' else self.event_location
        client = gmaps.Client(key=apikeys.GOOGLE_PLACES_API_KEY)
        response = places.find_place(client=client, input=location, fields=['place_id','geometry'], input_type='textquery')
        if response['status'] != 'OK':
            raise ValidationError("cannot find this address", code = "error")
        self.lattitude = response['candidates'][0]['geometry']['location']['lat']
        self.longitude = response['candidates'][0]['geometry']['location']['lng']
        self.placeID = response['candidates'][0]['place_id']
        
        self.city = self.religious_establishment.city if self.city == '' else self.city
        self.country = self.religious_establishment.country if self.country == '' else self.country 
        return super(event, self).save(*args, **kwargs)
    
    def can_view(self, user_model):
        if not self.private:
            return True
        return self.religious_establishment.can_view(user_model) or self.event_members.filter(id = user_model.id).exists()

    def add_request(self, user:UserModel):
        self.requests_to_join.add(user)
        self.save()
        
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
        elif invited:
            self.invited_users.remove(user)
            self.event_members.add(user)
            self.save()
        else:
            raise InvalidUserException()
    
    def remove_member(self, remover: UserModel, user:UserModel):
        admin = self.religious_establishment.admins.filter(id = remover.id).exists() or remover.id == user.id
        member_is_admin = self.religious_establishment.admins.filter(id = user.id).exists() and remover.id != user.id
        member = self.event_members.filter(id=user.id).exists()
        if not admin or member_is_admin:
            raise InvalidUserException()
        elif member:
            self.event_members.remove(user)
            self.save()
        else:
            return
        
    def __str__(self):
        return self.name