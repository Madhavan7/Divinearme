from typing import Any
from rest_framework.viewsets import ReadOnlyModelViewSet
from search.models.user_profile import UserModel
from search.models.invitation import TempleInvitation, EventInvitation
from search.serializers.invitation_serializer import TempleInvitationSerializer, EventInvitationSerializer
from rest_framework.response import Response
from rest_framework import status 
from search.paginators import custom_pagination
from django.core.exceptions import ObjectDoesNotExist

class InvitationView(ReadOnlyModelViewSet):
  invitation_class = TempleInvitation
  serializer_class = TempleInvitationSerializer
  pagination_class = custom_pagination

  def set_invitation_class(self, request, *args, **kwargs):
    isTemple = request.GET.get('temple', 1)
    print(isTemple)
    self.kwargs['invitation_class'] = TempleInvitation if isTemple else EventInvitation
    self.serializer_class = TempleInvitationSerializer if self.kwargs['invitation_class'] == TempleInvitation else EventInvitationSerializer
  
  def set_args(self, request, *args, **kwargs):
    if 'user_pk' in kwargs:
      self.kwargs['user_pk'] = kwargs['user_pk']
      self.kwargs['user'] = UserModel.objects.get(id = self.kwargs['user_pk'])
    else:
      self.kwargs.pop('user_pk')
      self.kwargs.pop('user')

  def get_queryset(self):
    try:
      return self.invitation_class.objects.get(user=self.kwargs['user']).all().order_by('invite_time')
    except ObjectDoesNotExist:
      return self.invitation_class.objects.none()
  
  def retrieve(self, request, *args, **kwargs):
    try:
      self.set_args(request, *args, **kwargs)
      self.set_invitation_class(request, *args, **kwargs)
      if request.user != self.kwargs['user'].user:
        return Response(data={'message':'you do not have this permission'}, status=status.HTTP_401_UNAUTHORIZED)
      else:
        super().retrieve(request, *args, **kwargs)
    except KeyError:
      return Response(status=status.HTTP_400_BAD_REQUEST)
  
  def list(self, request, *args, **kwargs):
    try:
      self.set_args(request, *args, **kwargs)
      self.set_invitation_class(request, *args, **kwargs)
      if request.user != self.kwargs['user'].user:
        return Response(data={'message':'you do not have this permission'}, status=status.HTTP_401_UNAUTHORIZED)
      else:
        return super().list(request, *args, **kwargs)
    except KeyError:
      return Response(status=status.HTTP_400_BAD_REQUEST)
