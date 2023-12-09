from django.db import models
from .user_profile import UserModel
from search.exceptions.exceptions import InvalidUserException
from django.forms import ValidationError
import googlemaps as gmaps
import googlemaps.places as places
import googlemaps.addressvalidation as addval
import search.apikeys as apikeys

class temple(models.Model):
    name = models.CharField(max_length=100)
    private = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    #location based parameters
    placeID = models.CharField(max_length = 200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    temple_location = models.CharField(max_length = 200)
    lattitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    #########################################
    date_joined = models.DateTimeField(auto_now_add=True)
    invited_users = models.ManyToManyField(UserModel, through='TempleInvitation')
    requests_to_join = models.ManyToManyField(UserModel, related_name="temple_requests", blank=True)
    temple_members = models.ManyToManyField(UserModel, related_name="temples", blank=True)
    admins = models.ManyToManyField(UserModel, related_name="admins")
    class Meta:
        ordering = ["date_joined"]

    def clean(self) -> None:
        client = gmaps.Client(key=apikeys.GOOGLE_PLACES_API_KEY)
        response = addval.addressvalidation(client=client, addressLines=[getattr(self,'temple_location')])
        addressComplete = response['result']['verdict'].get('addressComplete', False)
        if not addressComplete:
            raise ValidationError("incomplete address", code="incomplete-address")
        
        components = response['result']['address'].get('addressComponents', [])
        for component in components:
            if component['confirmationLevel'] != 'CONFIRMED':
                raise ValidationError("incorrect component " + component['componentType'] + ": " + component['confirmationLevel'], code="incorrect-component")

    def save(self, *args, **kwargs):
        client = gmaps.Client(key=apikeys.GOOGLE_PLACES_API_KEY)
        response = places.find_place(client=client, input=getattr(self, 'temple_location'), fields=['place_id','geometry'], input_type='textquery')
        if response['status'] != 'OK':
            raise ValidationError("cannot find this address", code = "error")
        self.placeID = response['candidates'][0]['place_id']
        self.longitude = response['candidates'][0]['geometry']['location']['lng']
        self.lattitude = response['candidates'][0]['geometry']['location']['lat']
        return super(temple, self).save(*args, **kwargs)
    
    def can_view(self, user_model):
        return not self.private or self.temple_members.all().filter(id = user_model.id).exists()
    
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
    
    def add_request(self, user:UserModel):
        self.requests_to_join.add(user)
        self.save()

    def remove_member(self, remover: UserModel, user:UserModel):
        admin = self.admins.all().filter(id = remover.id).exists() or remover.id == user.id
        member_is_admin = self.admins.all().filter(id = user.id).exists() and remover.id != user.id
        member = self.temple_members.all().filter(id=user.id).exists()
        if not admin or member_is_admin:
            raise InvalidUserException()
        elif member:
            self.temple_members.remove(user)
            self.save()
        else:
            return
    
    def remove_event(self, remover:UserModel, event):
        admin = self.admins.all().filter(id=remover.id).exists()
        if admin and self.events.all().filter(id=event.id).exists():
            event.delete()
        else:
            raise InvalidUserException()
        self.save()
    def __str__(self):
        return self.name