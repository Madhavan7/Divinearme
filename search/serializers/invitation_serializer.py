from rest_framework import serializers
from models.invitation import *


class temple_invitation_serializer(serializers.ModelSerializer):
    class Meta:
        model = temple_invitation
        fields = '__all__'

class event_invitation_serializer(serializers.ModelSerializer):
    class Meta:
        model = event_invitation
        fields = '__all__'