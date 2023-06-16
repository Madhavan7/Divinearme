from rest_framework import serializers

class comment_reply_serializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    text = serializers.CharField()
    date_added = serializers.DateTimeField()