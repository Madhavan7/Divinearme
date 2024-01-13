from rest_framework import serializers
from django.contrib.auth.models import User
from search.models.user_profile import UserModel

class MemberSerializer(serializers.ModelSerializer):
    #method_name will be get_username
    username = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = '__all__'
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    
    def get_username(self, obj:UserModel):
        return obj.user.username