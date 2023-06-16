from rest_framework import serializers
import post_serializer

class member_serializer(serializers.Serializer):
    name = serializers.CharField(max_length= 200)
    email = serializers.EmailField()
    biography = serializers.CharField()
    date_joined = serializers.DateTimeField()
    posts = post_serializer(many = True)