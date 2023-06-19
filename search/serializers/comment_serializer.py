from rest_framework import serializers

from search.models.posts import comment

class comment_serializer(serializers.Serializer):
    class Meta:
        model = comment
        fields = '__all__'