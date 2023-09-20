from rest_framework import serializers

from search.models.posts import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = post
        fields = ['title','poster', 'username', 'text', 'date_added']

class TemplePostSerializer(serializers.ModelSerializer):
    class Meta(PostSerializer.Meta):
        model = TemplePost
        fields = ['title','poster', 'username', 'text', 'date_added', 'templeID']

class EventPostSerializer(serializers.ModelSerializer):
    class Meta(PostSerializer.Meta):
        model = EventPost
        fields = ['title','poster', 'username', 'text', 'date_added', 'eventID']