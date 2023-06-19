from rest_framework import serializers
from search.models.posts import commentReply

class comment_reply_serializer(serializers.Serializer):
    class Meta:
        model = commentReply
        fields = '__all__'