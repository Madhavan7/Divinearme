from rest_framework import viewsets
from search.serializers.event_serializer import EventSerializer
from search.models.temple import temple
from search.models.event import event
from search.models.user_profile import UserModel

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = event.objects.all()
    def get_queryset(self):
        #have to check permissions
        if 'temple_pk' in self.kwargs:
            return temple.objects.get(id = self.kwargs['temple_pk']).events.all()
        if 'user_pk' in self.kwargs:
            return UserModel.objects.get(id = self.kwargs['user_pk']).events.all()
        return super().get_queryset()