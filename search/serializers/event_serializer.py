from rest_framework import serializers

import member_serializer
import post_serializer

class event_serializer(serializers.Serializer):
    name = serializers.CharField(max_length= 200)
    location = serializers.CharField(max_length=200)
    description = serializers.CharField()
    date = serializers.DateField()
    date_joined = serializers.DateTimeField()
    members = member_serializer(many = True)
    posts = post_serializer(many = True)