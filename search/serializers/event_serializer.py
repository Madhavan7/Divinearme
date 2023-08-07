from rest_framework import serializers
from search.models.event import event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ['name', 'religious_establishment', 'description', 'date', 'date_joined']