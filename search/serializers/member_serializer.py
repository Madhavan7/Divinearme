from rest_framework import serializers
from search.models.user_profile import UserModel

class MemberSerializer(serializers.ModelSerializer):
    #method_name will be get_username
    username = serializers.SerializerMethodField()
    class Meta:
        model = UserModel
        fields = '__all__'
    
    def get_username(self, obj:UserModel):
        return obj.user.username