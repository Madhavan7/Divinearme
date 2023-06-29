from requests import Response
from rest_framework import views
from serializers.event_serializer import event_serializer
from serializers.temple_serializer import temple_serializer
from serializers.member_serializer import member_serializer
from serializers.invitation_serializer import *
from django.contrib.auth.models import User

class login_view(views.APIView):
    serializer_class = member_serializer
    queryset = User.objects.all()

    def render_user(self, user:User, response:dict):
        #need to implement pagination
        response['temples'] = temple_serializer(queryset = user.temples.all().order_by("name")[:3], many = True)
        response['events'] = event_serializer(queryset = user.events.all().order_by("-start_date_time")[:3], many = True)
        response['temple_invitations'] = temple_invitation_serializer(queryset = user.temple_invitations.all().order_by("-invite_time")[:3], many = True)
        response['event_invitations'] = temple_invitation_serializer(queryset = user.event_invitations.all().order_by("-invite_time")[:3], many = True)
        response['temple_requests'] = temple_serializer(queryset = user.objects.all().order_by("name")[:3], many = True)

    def post(self, request):
        error_response = Response({request.data}.copy())
        #do research if there are more efficient ways to achieve the below
        try:
            user = self.queryset.filter(username = request['username'], password = request['password'])
        except KeyError:
            if 'username' not in request.data:
                error_response['error(username)'] = 'please enter a username'
            if 'password' not in request.data:
                error_response['error(password)'] = 'please enter a password'
            #have to fix below
            error_response.status_code = 'HTTP_400_BAD_REQUEST'
            return error_response
        except User.DoesNotExist:
            error_response.status_code = 'HTTP_401_UNAUTHORIZED'
            error_response['error(user does not exist)'] = 'please enter a valid username and password'
            return error_response
        else:
            serializer = self.serializer_class(user)
            response_dict = serializer.data.copy()
            #get temples
            self.render_user(user, response_dict)
            return Response(response_dict)