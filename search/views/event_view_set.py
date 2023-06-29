from rest_framework import viewsets
from serializers.event_serializer import event_serializer
from models.temple import temple
from models.event import event
from django.contrib.auth.models import User

class event_view_set(viewsets.ModelViewSet):
    serializer_class = event_serializer
    queryset = event.objects.all()
    def get_queryset(self):
        if 'temple_pk' in self.kwargs:
            return temple.objects.get(id = self.kwargs['temple_pk']).events.all()
        if 'user_pk' in self.kwargs:
            return User.objects.get(id = self.kwargs['user_pk']).events.all()
        return super().get_queryset()