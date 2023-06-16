from rest_framework import serializers

import comment_reply_serializer

class comment_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    text = serializers.CharField()
    date_added = serializers.DateTimeField()
    comment_reply = comment_reply_serializer(many=True)