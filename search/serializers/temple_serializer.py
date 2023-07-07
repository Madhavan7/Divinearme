from rest_framework import serializers
from search.models.temple import temple
from django.contrib.auth.models import AnonymousUser
from search.models.user_profile import user_model
from .event_serializer import event_serializer

class temple_cu_serializer(serializers.ModelSerializer):
    class Meta:
        model = temple
        fields = ['name', 'description', 'date_joined', ]

class temple_serializer(serializers.ModelSerializer):
    def create(self, validated_data):
        temp = super().create(validated_data)
        request = self.context.get("request")
        #need to debug below
        if request and hasattr(request, "user") and not isinstance(request.user, AnonymousUser):
            u_model = user_model.objects.get(user = request.user)
            temp.temple_members.add(u_model)
            temp.admins.add(u_model)
        temp.save()
        return temp
    class Meta:
        model = temple
        fields = ['name', 'description', 'date_joined',]