from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from search.exceptions.exceptions import InvalidUserException
from search.models.posts import post
from search.serializers.event_serializer import EventSerializer
from search.serializers.post_serializer import PostSerializer
from search.models.temple import temple
from search.models.event import event
from search.models.user_profile import UserModel
from .view_builders.event_view_builder import *
import search.permissions.temple_permissions as temple_perm
import search.permissions.event_permissions as event_perm
from rest_framework.serializers import ValidationError
from typing import List
import json as json

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = post.objects.all()

    def set_args(self, request, *args, **kwargs):
        #Gotta add seperate if statements for users
        if 'event_pk' in kwargs:
            self.kwargs['event_pk'] = kwargs['event_pk']
            temp = event.objects.get(id = self.kwargs['event_pk'])
            if not event_perm.EventViewPermission().has_object_permission(request, None, temp):
                raise InvalidUserException()
        elif 'event_pk' in self.kwargs:
            self.kwargs.pop('event_pk')
        
        if 'temple_pk' in kwargs:
            self.kwargs['temple_pk'] = kwargs['temple_pk']
            temp = temple.objects.get(id = self.kwargs['temple_pk'])
            if not temple_perm.TempleViewPermission().has_object_permission(request, None, temp):
                raise InvalidUserException()
        elif 'temple_pk' in self.kwargs:
            self.kwargs.pop('temple_pk')
        return None
    
    def get_queryset(self):
        #gotta add seperate if statements for users
        if 'temple_pk' in self.kwargs:
            #temp = temple.objects.get(id = self.kwargs['temple_pk'])
            return temple.objects.get(id = self.kwargs['temple_pk']).events.all()
        if 'event_pk' in self.kwargs:
            return UserModel.objects.get(id = self.kwargs['event_pk']).events.all()
        return super().get_queryset()