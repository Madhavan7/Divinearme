from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from search.serializers.event_serializer import EventSerializer
from search.models.temple import temple
from search.models.event import event
from search.models.user_profile import UserModel
import search.permissions.temple_permissions as temple_perm
from rest_framework.serializers import ValidationError
class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = event.objects.all()
    def get_queryset(self):
        #have to check permissions
        #assumes that kwargs does not contain both
        if 'temple_pk' in self.kwargs:
            return temple.objects.get(id = self.kwargs['temple_pk']).events.all()
        if 'user_pk' in self.kwargs:
            return UserModel.objects.get(id = self.kwargs['user_pk']).events.all()
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        if 'user_pk' in kwargs:
            self.kwargs['user_pk'] = kwargs['user_pk']
        elif 'user_pk' in self.kwargs:
            self.kwargs.pop('user_pk')
        
        if 'temple_pk' in kwargs:
            self.kwargs['temple_pk'] = kwargs['temple_pk']
        elif 'temple_pk' in self.kwargs:
            self.kwargs.pop('temple_pk')
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        #I have to find a way to make sure exceptions give the right messages
        #Working alright right now, have to find a way to make start date time compulsory
        try: 
            #Query dict instance is immutable
            req = request.data.copy()
            req['religious_establishment'] = kwargs['temple_pk']
            admin = temple_perm.TempleUpdatePermission().has_object_permission(request, None, temple.objects.get(id=req['religious_establishment']))
            if not admin:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(data=req)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as val:
            errors = val.detail
            return Response(errors, status=status.HTTP_401_UNAUTHORIZED)

    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)