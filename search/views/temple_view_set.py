from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from search.exceptions.exceptions import InvalidUserException
from search.serializers.temple_serializer import TempleSerializer
from search.models.temple import temple
from search.models.user_profile import UserModel
from search.models.event import event
from search.views.view_builders.temple_search_strategy import TempleSearchStrategy
from search.paginators import custom_pagination
from search.permissions.temple_permissions import TempleUpdatePermission
from typing import List
import json as json
from django.db import IntegrityError, transaction

from search.views.view_builders.temple_view_builder import TempleViewDirector

class TempleViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TempleSerializer
    queryset = temple.objects.all()
    pagination_class = custom_pagination

    def add_members(self, request, instance, name):
        if name not in request.data:
            return instance
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
    
    def remove_members(self, request, instance):
        if "remove_members" not in request.data:
            return instance
        remover = UserModel.objects.get(user=request.user)
        names = json.loads(request.data["remove_members"])
        if not isinstance(names, List):
            return instance
        for ser in names:
            if isinstance(ser, dict) and "user" in ser:
                try:
                    u_model = UserModel.objects.get(user=ser["user"])
                    instance.remove_member(remover, u_model)
                except UserModel.DoesNotExist:
                    continue
        return instance
    
    def remove_events(self, request, instance):
        if "remove_events" not in request.data:
            return instance
        remover = UserModel.objects.get(user=request.user)
        events = json.loads(request.data["remove_events"])
        if not isinstance(events, List):
            return instance
        for even in events:
            if isinstance(even, dict) and "id" in even:
                try:
                    even2 = event.objects.get(id=even["id"])
                    instance.remove_event(remover, even2)
                except event.DoesNotExist:
                    continue
        return instance
    
    def add_get_params(self, request, *args, **kwargs):
        for param in request.GET:
            self.kwargs[param] = request.GET.get(param, None)

    def get_queryset(self):
        #Need protections because not everybody can view user
        return TempleSearchStrategy().search(self.kwargs)
    
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
            if request.user.id != int(self.kwargs['user_pk']):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        #elif 'user_pk' in self.kwargs:
            #self.kwargs.pop('user_pk')
        self.add_get_params(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        #at the serializer level, the user created will be added as admin
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as i:
            return Response(data= {'message': str(i)},status=status.HTTP_403_FORBIDDEN)
        except InvalidUserException as i:
            return Response(data= {'message': str(i)},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        #may need a helper function 
        #only way you can update is if admin
        #have to deal with adding members 
        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            if not TempleUpdatePermission().has_object_permission(request, None, instance):
                return Response(status = status.HTTP_401_UNAUTHORIZED)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            #Dealing with adding member
            #now that I think about it its better if the check is done inside the function body
            with transaction.atomic():
                self.add_members(request, instance, "temple_members")
                self.add_members(request, instance, "admins")
                self.remove_members(request, instance)
                instance.save()
            return Response(serializer.data)
        except InvalidUserException:
            return Response(status = status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        #currently all admins can destroy the temple which is a flaw, maybe can add a king admin
        temp = self.get_object()
        if not TempleUpdatePermission().has_object_permission(request, None, temp):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            self.perform_destroy(temp)
            return Response(status=status.HTTP_204_NO_CONTENT)
        

