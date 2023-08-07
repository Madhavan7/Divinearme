from rest_framework import serializers

from search.models.posts import post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = ['title','poster', 'username', 'text', 'date_added']