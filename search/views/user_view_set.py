from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from search.serializers.invitation_serializer import *
from search.serializers.temple_serializer import temple_serializer
from search.models.temple import temple
from django.contrib.auth.models import User
from search.paginators import custom_pagination
from search.serializers.member_serializer import member_serializer
from search.serializers.event_serializer import event_serializer

class user_view_set(ModelViewSet):
    serializer_class = member_serializer
    queryset = User.objects.all()
    pagination_class = custom_pagination

    def get_queryset(self):
        return super().get_queryset()

    def render_user(self, user:User, response:dict):
        #need to implement pagination
        response['temples'] = temple_serializer(queryset = user.temples.all().order_by("name")[:3], many = True)
        response['events'] = event_serializer(queryset = user.events.all().order_by("-start_date_time")[:3], many = True)
        response['temple_invitations'] = temple_invitation_serializer(queryset = user.temple_invitations.all().order_by("-invite_time")[:3], many = True)
        response['event_invitations'] = temple_invitation_serializer(queryset = user.event_invitations.all().order_by("-invite_time")[:3], many = True)
        response['temple_requests'] = temple_serializer(queryset = user.objects.all().order_by("name")[:3], many = True)

    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)