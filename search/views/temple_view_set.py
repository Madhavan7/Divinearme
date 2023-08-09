from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from search.exceptions.exceptions import InvalidUserException
from search.serializers.temple_serializer import TempleSerializer
from search.models.temple import temple
from search.models.user_profile import UserModel
from search.models.event import event
from search.paginators import custom_pagination
from typing import List
import json as json

from search.views.view_builders.temple_view_builder import TempleViewDirector

class TempleViewSet(ModelViewSet):
    serializer_class = TempleSerializer
    queryset = temple.objects.all()
    pagination_class = custom_pagination

    def add_members(self, request, instance, name):
        adder = UserModel.objects.get(user = request.user)
        #adding members to the queryset
        names = json.loads(request.data[name])
        if not isinstance(names, List):
            return instance
        for ser in names:
            if isinstance(ser, dict) and "user" in ser:
                try:
                    u_model = UserModel.objects.get(user = ser["user"])
                    instance.add_member(adder, u_model, name)
                except UserModel.DoesNotExist:
                    continue
        return instance
    
    def add_events(self, request, instance):
        adder = UserModel.objects.get(user = request.user)
        events = json.loads(request.data["events"])
        if not isinstance(events, List):
            return instance
        for e in events:
            if isinstance(e, dict) and "id" in e:
                try:
                    even = event.objects.get(id = e["id"])
                    instance.add_event(adder, even)
                except event.DoesNotExist:
                    continue
        return instance


    def get_queryset(self):
        if 'user_pk' in self.kwargs:
            #have to check permissions
            return UserModel.objects.get(id=self.kwargs['user_pk']).temples.all()
        return super().get_queryset()
    
    #overriding this, since temple serializer is not enough info for temple view
    def retrieve(self, request, *args, **kwargs):
        #gotta edit this to make it more detailed
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        resp = serializer.data
        temple_builder = TempleViewDirector(request, instance)
        temple_builder.build(instance, resp)
        return Response(resp)
    
    def list(self, request, *args, **kwargs):
        if 'user_pk' in kwargs:
            self.kwargs['user_pk'] = kwargs['user_pk']
        elif 'user_pk' in self.kwargs:
            self.kwargs.pop('user_pk')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        #at the serializer level, the user created will be added as admin
        try:
            return super().create(request, *args, **kwargs)
        except InvalidUserException():
            #really dont need this, as the permissions are IsAuthenticatedOrReadOnly
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        #may need a helper function 
        #only way you can update is if admin
        #have to deal with adding members 
        try:
            partial = kwargs.pop('partial', True)
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
            if "temple_members" in request.data:
                print(request.data["temple_members"])
                self.add_members(request, instance, "temple_members")
            if "admins" in request.data:
                self.add_members(request, instance, "admins")
            
            #adding events
            if "events" in request.data:
                self.add_events(request, instance)
            instance.save()
            return Response(serializer.data)
        except InvalidUserException:
            return Response(status = status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        #only way to destroy is to be an admin
        #have to deal with deleting members
        try:
            return super().destroy(request, *args, **kwargs)
        except InvalidUserException:
            return Response(status = status.HTTP_401_UNAUTHORIZED)
        

