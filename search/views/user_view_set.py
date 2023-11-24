from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
import search.permissions.temple_permissions as temple_perm
import search.permissions.event_permissions as event_perm
from search.exceptions.exceptions import InvalidUserException
from search.serializers.invitation_serializer import *
from search.serializers.temple_serializer import TempleSerializer
from search.models.temple import temple
from search.paginators import custom_pagination
from search.serializers.member_serializer import MemberSerializer
from search.serializers.event_serializer import EventSerializer
from django.db import transaction

class UserViewSet(ModelViewSet):
    #authentication_classes = []
    serializer_class = MemberSerializer
    queryset = UserModel.objects.all()
    pagination_class = custom_pagination
    temple = None
    event = None
    def set_args(self, request, *args, **kwargs):
        self.kwargs['join_request'] = request.GET.get('join_request', 0)
        if 'temple_pk' in kwargs:
            self.kwargs['temple_pk'] = kwargs['temple_pk']
            temp = temple.objects.get(id = self.kwargs['temple_pk'])
            if not temple_perm.TempleViewPermission().has_object_permission(request, None, temp):
                raise InvalidUserException("cannot view temple")
            elif self.kwargs['join_request'] and not temple_perm.TempleUpdatePermission().has_object_permission(request, None, temp):
                raise InvalidUserException("cannot view requests")
            return
        elif 'temple_pk' in self.kwargs:
            self.kwargs.pop('temple_pk')
        
        if 'event_pk' in kwargs:
            self.kwargs['event_pk'] = kwargs['event_pk']
            temp = event.objects.get(id = self.kwargs['event_pk'])
            if not event_perm.EventViewPermission().has_object_permission(request, None, temp):
                raise InvalidUserException("cannot view event")
            elif self.kwargs['join_request'] and not event_perm.EventUpdatePermission().has_object_permission(request, None, temp):
                raise InvalidUserException("cannot view requests")
            return
        elif 'event_pk' in self.kwargs:
            self.kwargs.pop('event_pk')
        
    def get_queryset(self):
        if 'temple_pk' in self.kwargs:
            if not self.kwargs['join_request']:
                return temple.objects.get(id=self.kwargs['temple_pk']).temple_members.all()
            else:
                return temple.objects.get(id=self.kwargs['temple_pk']).requests_to_join.all()
        
        if 'event_pk' in self.kwargs:
            if not self.kwargs['join_request']:
                return event.objects.get(id=self.kwargs['event_pk']).event_members.all()
            else:
                return event.objects.get(id=self.kwargs['event_pk']).requests_to_join.all()
        return super().get_queryset()

    def render_user(self, user:UserModel, response:dict):
        response['include'] = ['temples', 'events', 'temple_invitations', 'event_invitations', 'temple_requests', 'event_requests']
    

    def retrieve(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            user = self.get_object()
            response_dict = self.get_serializer(user).data
            response_dict['include'] = []
            if request.user != user.user:
                return Response(response_dict)
            else:
                self.render_user(user, response_dict)
            return Response(response_dict)
        except InvalidUserException as i:
            return Response(data= {'message': str(i)},status=status.HTTP_401_UNAUTHORIZED)
    

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                req = request.data.copy()
                user = User.objects.create(username = req.get('username', None), password = req.get('password', None))
                user.set_password(req.get('password', None))
                user.save()
                req['user'] = user.id
                serializer = self.get_serializer(data = req)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except IntegrityError as i:
            return Response(data= {'message': str(i)},status=status.HTTP_400_BAD_REQUEST)
        except InvalidUserException as i:
            return Response(data= {'message': str(i)},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        self.set_args(request, *args, **kwargs)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        req = request.data.copy()
        if instance.user.id != request.user.id:
            return Response(data={'message': 'you do not have this permission'}, status=status.HTTP_403_FORBIDDEN)
        try:
            with transaction.atomic():
                instance_user = User.objects.get(id = instance.user.id)
                instance_user.username = req.get('username', instance_user.username)
                if 'password' in req:
                    instance_user.set_password(req['password'])
                instance_user.save()
                serializer = self.get_serializer(instance, data=req, partial=partial)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response(serializer.data)
        except IntegrityError as i:
            return Response(data= {'message': str(i)},status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            instance = self.get_object()
            if instance.user.id != request.user.id:
                return Response(data={'message': 'you do not have this permission'}, status=status.HTTP_403_FORBIDDEN)
            instance.user.delete()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvalidUserException:
            return Response(data= {'message': 'you do not have this permission'},status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            #queryset must change depending on whether temple or event pk is in kwargs
            return super().list(request, *args, **kwargs)
        except InvalidUserException as i:
            return Response(data= {'message': str(i)},status=status.HTTP_401_UNAUTHORIZED)
