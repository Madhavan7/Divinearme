from rest_framework import serializers

from search.models.posts import post

class post_serializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = ['poster', 'username', 'text', 'date_added']