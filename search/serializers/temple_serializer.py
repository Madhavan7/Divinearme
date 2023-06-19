from rest_framework import serializers
from search.models.temple import temple
from .event_serializer import event_serializer
class temple_serializer(serializers.ModelSerializer):
    temple_members = serializers.StringRelatedField(many=True, source = "less_members")
    events = event_serializer(many=True, source="less_events")
    class Meta:
        model = temple
        fields = ['name', 'temple_members', 'description', 'date_joined', 'events']