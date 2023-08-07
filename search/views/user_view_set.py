from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from search.serializers.invitation_serializer import *
from search.serializers.temple_serializer import TempleSerializer
from search.models.temple import temple
from search.paginators import custom_pagination
from search.serializers.member_serializer import MemberSerializer
from search.serializers.event_serializer import EventSerializer

class UserViewSet(ModelViewSet):
    serializer_class = MemberSerializer
    queryset = UserModel.objects.all()
    pagination_class = custom_pagination
    temple = None
    event = None
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
        user = self.get_object()
        response_dict = self.get_serializer(user).data
        if request.user != user:
            return Response(response_dict)
        else:
            self.render_user(user, response_dict)
        return Response(response_dict)
    
    def list(self, request, *args, **kwargs):
        #queryset must change depending on whether temple or event pk is in kwargs
        if 'temple_pk' in kwargs:
            self.kwargs['temple_pk'] = kwargs['temple_pk']
        elif 'temple_pk' in self.kwargs:
            self.kwargs.pop('temple_pk')
        
        if 'event_pk' in kwargs:
            self.kwargs['event_pk'] = kwargs['event_pk']
        elif 'event_pk' in self.kwargs:
            self.kwargs.pop('event_pk')

        return super().list(request, *args, **kwargs)