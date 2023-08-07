from rest_framework import serializers
from search.models.invitation import *


class TempleInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempleInvitation
        fields = '__all__'

class EventInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInvitation
        fields = '__all__'