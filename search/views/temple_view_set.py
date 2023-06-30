from rest_framework import viewsets
from serializers.temple_serializer import temple_serializer
from models.temple import temple
from django.contrib.auth.models import User
from paginators import custom_pagination
from requests import Response
from serializers.member_serializer import member_serializer
from serializers.event_serializer import event_serializer

class temple_view_set(viewsets.ModelViewSet):
    serializer_class = temple_serializer
    queryset = temple.objects.all()
    pagination_class = custom_pagination

    def get_queryset(self):
        if 'user_pk' in self.kwargs:
            return User.objects.get(id=self.kwargs['user_pk']).temples.all()
        return super().get_queryset()
    
    #adds the info to the response - the info needed to render the temple
    def render_temple(self, temp:temple, response:dict):
        response['events'] = event_serializer(queryset = temp.events.all().order_by('start_date')[:5], many = True)
    
    #below is when the user is in the temple, so we can show more fields
    def render_temple_detailed(self, temp:temple, response:dict):
        self.render_temple(temp, response)
        response['temple_members'] = member_serializer(queryset = temp.temple_members.all().order_by['name'][:5], many = True)

    #below is when the user is the admin of the temple
    def render_temple_admin(self, temp:temple, response:dict):
        self.render_temple_detailed(temp, response)
        response['invited_users'] = member_serializer(queryset = temp.invited_users.all().order_by['-invited_time'][:5], many = True)
        response['requested_users'] = member_serializer(queryset = temp.requests_to_join.all().order_by['-invited_time'][:5], many = True)
    
    #overriding this, since temple serializer is not enough info for temple view
    def retrieve(self, request, *args, **kwargs):
        
        if 'user_pk' in kwargs:
            self.kwargs['user_pk'] = kwargs['user_pk']
        elif 'user_pk' in self.kwargs:
            self.kwargs.pop('user_pk')

        temp = self.get_object()
        response_dict = self.get_serializer(temp).data
        if temp.private and request.user not in temp.temple_members.all():
            return Response(response_dict)
        else:
            if request.user in temp.admins.all():
                self.render_temple_admin(temp, response_dict)
            else:
                self.render_temple(temp, response_dict)
            return Response(response_dict)
        

