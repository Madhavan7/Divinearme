from rest_framework import serializers
from search.models.event import event

class event_serializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ['name', 'religious_establishment', 'description', 'date', 'date_joined']