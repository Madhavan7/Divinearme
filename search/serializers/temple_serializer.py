from rest_framework import serializers
from search.models.temple import temple
from .event_serializer import event_serializer

class temple_cu_serializer(serializers.ModelSerializer):
    class Meta:
        model = temple
        fields = ['name', 'description', 'date_joined', ]

class temple_serializer(serializers.ModelSerializer):
    class Meta:
        model = temple
        fields = ['name', 'description', 'date_joined',]