from rest_framework import serializers

from search.models.posts import comment

class CommentSerializer(serializers.Serializer):
    class Meta:
        model = comment
        fields = '__all__'