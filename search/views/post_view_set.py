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
from search.models.posts import *
from .view_builders.event_view_builder import *
import search.permissions.temple_permissions as temple_perm
import search.permissions.event_permissions as event_perm
from rest_framework.serializers import ValidationError
from typing import Any, List
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
            return TemplePost.objects.get(templeID = self.kwargs['temple_pk']).events.all()
        if 'event_pk' in self.kwargs:
            return EventPost.objects.get(eventID = self.kwargs['event_pk']).events.all()
        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            can_post = temple_perm.TemplePostCommentPermission().has_object_permission(request, *args, **kwargs) if "temple_pk" in self.kwargs else event_perm.EventPostCommentPermission().has_object_permission(request, *args, **kwargs)
            if not can_post:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            req = request.data.copy()
            req["commenter"] = UserModel.objects.get(user=request.user).id
            serializer = self.get_serializer(data=req)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except KeyError or UserModel.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as val:
            errors = val.detail
            return Response(errors, status=status.HTTP_401_UNAUTHORIZED)
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)