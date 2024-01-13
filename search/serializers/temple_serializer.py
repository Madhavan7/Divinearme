from rest_framework import serializers
from django.forms import ValidationError
import search.apikeys as apikeys
import googlemaps as gmaps
import googlemaps.addressvalidation as addval
from search.exceptions.exceptions import InvalidUserException
from search.models.temple import temple
from django.contrib.auth.models import AnonymousUser
from search.models.user_profile import UserModel
import search.permissions.temple_permissions as perm

class TempleSerializer(serializers.ModelSerializer):
    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
    def create(self, validated_data):
        request = self.context.get("request")
        #need to debug below
        if request and hasattr(request, "user") and not isinstance(request.user, AnonymousUser):
            temp = super().create(validated_data)
            u_model = UserModel.objects.get(user = request.user)
            temp.temple_members.add(u_model)
            temp.admins.add(u_model)
            temp.save()
            return temp
        else:
            #really dont need this as the permissions are IsAuthenticatedOrReadOnly
            raise InvalidUserException()
    def update(self, instance, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user") and not isinstance(request.user, AnonymousUser):
            if perm.TempleUpdatePermission().has_object_permission(request, None, instance):
                return super().update(instance, validated_data)
            else:
                raise InvalidUserException()
        raise InvalidUserException()

    def validate_temple_location(self, value):
        client = gmaps.Client(key=apikeys.GOOGLE_PLACES_API_KEY)
        response = addval.addressvalidation(client=client, addressLines=[value])
        addressComplete = response['result']['verdict'].get('addressComplete', False)
        if not addressComplete:
            raise ValidationError("incomplete address", code="incomplete-address")
        for component in response['result']['address']['addressComponents']:
            if component['confirmationLevel'] != 'CONFIRMED':
                raise ValidationError("incorrect component " + component['componentType'] + ": " + component['confirmationLevel'], code="incorrect-component")
        return value

        
    class Meta:
        model = temple
        fields = ['id','name', 'description', 'date_joined','temple_location']