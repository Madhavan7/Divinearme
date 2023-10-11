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

class UserViewSet(ModelViewSet):
    authentication_classes = []
    serializer_class = MemberSerializer
    queryset = UserModel.objects.all()
    pagination_class = custom_pagination
    temple = None
    event = None
    def set_args(self, request, *args, **kwargs):
        if 'temple_pk' in kwargs:
            print('temple in kwargs')
            self.kwargs['temple_pk'] = kwargs['temple_pk']
            temp = temple.objects.get(id = self.kwargs['temple_pk'])
            if not temple_perm.TempleViewPermission().has_object_permission(request, None, temp):
                print("cant access temple")
                raise InvalidUserException("cannot view temple")
            return
        elif 'temple_pk' in self.kwargs:
            print('temple not in kwargs')
            self.kwargs.pop('temple_pk')
        
        if 'event_pk' in kwargs:
            self.kwargs['event_pk'] = kwargs['event_pk']
            temp = event.objects.get(id = self.kwargs['event_pk'])
            if not event_perm.EventViewPermission().has_object_permission(request, None, temp):
                print("cant access event")
                raise InvalidUserException("cannot view event")
            return
        elif 'event_pk' in self.kwargs:
            self.kwargs.pop('event_pk')
        
    def get_queryset(self):
        if 'temple_pk' in self.kwargs:
            return temple.objects.get(id=self.kwargs['temple_pk']).temple_members.all()
        
        if 'event_pk' in self.kwargs:
            return event.objects.get(id=self.kwargs['event_pk']).event_members.all()
        return super().get_queryset()

    def render_user(self, user:UserModel, response:dict):
        response['temples'] = TempleSerializer(queryset = UserModel.temples.all().order_by("name")[:3], many = True)
        response['events'] = EventSerializer(queryset = UserModel.events.all().order_by("-start_date_time")[:3], many = True)
        response['temple_invitations'] = TempleInvitationSerializer(queryset = UserModel.temple_invitations.all().order_by("-invite_time")[:3], many = True)
        response['event_invitations'] = TempleInvitationSerializer(queryset = UserModel.event_invitations.all().order_by("-invite_time")[:3], many = True)
        response['temple_requests'] = TempleSerializer(queryset = UserModel.objects.all().order_by("name")[:3], many = True)

    def retrieve(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            user = self.get_object()
            response_dict = self.get_serializer(user).data
            if request.user != user:
                return Response(response_dict)
            else:
                self.render_user(user, response_dict)
            return Response(response_dict)
        except InvalidUserException as i:
            return Response(data= {'message': str(i)},status=status.HTTP_401_UNAUTHORIZED)
    
    def create(self, request, *args, **kwargs):
        try:
            req = request.data.copy()
            user = User.objects.create(username = req.get('username', None), password = req.get('password', None))
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
    
    def list(self, request, *args, **kwargs):
        try:
            self.set_args(request, *args, **kwargs)
            #queryset must change depending on whether temple or event pk is in kwargs
            return super().list(request, *args, **kwargs)
        except InvalidUserException as i:
            return Response(data= {'message': str(i)},status=status.HTTP_401_UNAUTHORIZED)
