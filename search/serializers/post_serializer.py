from rest_framework import serializers

import comment_serializer

class post_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    text = serializers.CharField()
    date_added = serializers.DateTimeField()
    comments = comment_serializer(many=True)