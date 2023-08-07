from rest_framework import serializers
from search.models.posts import CommentReply

class CommentReplySerializer(serializers.Serializer):
    class Meta:
        model = CommentReply
        fields = '__all__'