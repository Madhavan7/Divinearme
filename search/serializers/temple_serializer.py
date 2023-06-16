from rest_framework import serializers

import post_serializer
import member_serializer
import event_serializer

class temple_serializer(serializers.Serializer):
    name = serializers.CharField(max_length= 200)
    location = serializers.CharField(max_length=200)
    description = serializers.CharField()
    date_joined = serializers.DateTimeField()
    members = member_serializer(many = True)
    events = event_serializer(many = True)
    posts = post_serializer(many = True)