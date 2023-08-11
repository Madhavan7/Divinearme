from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from search.exceptions.exceptions import InvalidUserException
from search.serializers.event_serializer import EventSerializer
from search.models.temple import temple
from search.models.event import event
from search.models.user_profile import UserModel
from .view_builders.event_view_builder import *
import search.permissions.temple_permissions as temple_perm
from rest_framework.serializers import ValidationError
from typing import List
import json as json

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = event.objects.all()
    def set_args(self, request, *args, **kwargs):
        if 'user_pk' in kwargs:
            self.kwargs['user_pk'] = kwargs['user_pk']
        elif 'user_pk' in self.kwargs:
            self.kwargs.pop('user_pk')
        
        if 'temple_pk' in kwargs:
            self.kwargs['temple_pk'] = kwargs['temple_pk']
            temp = temple.objects.get(id = self.kwargs['temple_pk'])
            if not temple_perm.TempleViewPermission().has_object_permission(request, None, temp):
                raise InvalidUserException()
        elif 'temple_pk' in self.kwargs:
            self.kwargs.pop('temple_pk')
        return None
    
    def get_queryset(self):
        #have to check permissions
        #assumes that kwargs does not contain both
        if 'temple_pk' in self.kwargs:
            #temp = temple.objects.get(id = self.kwargs['temple_pk'])
            return temple.objects.get(id = self.kwargs['temple_pk']).events.all()
        if 'user_pk' in self.kwargs:
            return UserModel.objects.get(id = self.kwargs['user_pk']).events.all()
        return super().get_queryset()

    def add_members(self, request, instance):
        adder = UserModel.objects.get(user = request.user)
        #adding members to the queryset
        names = json.loads(request.data["event_members"])
        if not isinstance(names, List):
            return instance
        for ser in names:
            if isinstance(ser, dict) and "user" in ser:
                try:
                    u_model = UserModel.objects.get(user = ser["user"])
                    instance.add_members(adder, u_model)
                except UserModel.DoesNotExist:
                    continue
        return instance

    def list(self, request, *args, **kwargs):
        #gotta complete this to make sure that viewing priviliges are considered
        #temple case is done now have to work on the user case
        #invalid is None if and only if person does not have viewing priviliges
        try:
            self.set_args(request, *args, **kwargs)
            super().list(request, *args, **kwargs)
        except InvalidUserException():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            resp = serializer.data
            event_builder = EventViewDirector(instance, request)
            event_builder.build(instance, resp)
        except InvalidUserException():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(resp)
    
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

    def update(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            partial = kwargs.pop('partial', True)
            #below will call invalid user exception when user does not have priviliges to view the list
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            #Dealing with adding member
            #now that I think about it its better if the check is done inside the function body
            if "event_members" in request.data:
                self.add_members(request, instance)
            instance.save()
            return Response(serializer.data)
        except InvalidUserException:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
    

    def destroy(self, request, *args, **kwargs):
        even = self.get_object()
        if not EventUpdatePermission().has_object_permission(request, None, even):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            self.perform_destroy(even)
            return Response(status=status.HTTP_204_NO_CONTENT)