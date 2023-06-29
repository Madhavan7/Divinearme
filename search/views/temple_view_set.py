from rest_framework import viewsets
from serializers.temple_serializer import temple_serializer
from models.temple import temple
from django.contrib.auth.models import User

class temple_view_set(viewsets.ModelViewSet):
    serializer_class = temple_serializer
    queryset = temple.objects.all()

    def get_queryset(self):
        if 'user_pk' in self.kwargs:
            return User.objects.get(id=self.kwargs['user_pk']).temples.all()
        return super().get_queryset()