from rest_framework import serializers
from search.models.event import event

class EventSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return super().create(validated_data)
    class Meta:
        model = event
        fields = ['name', 'religious_establishment', 'description', 'start_date_time', 'end_date_time', 'date_joined']