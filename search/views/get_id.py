from rest_framework.response import Response
from rest_framework import status
from search.models.user_profile import UserModel
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_id(request):
  #Should I make this request.id
  if request.user.id:
    id = str(UserModel.objects.get(user= request.user).id)
    return Response(data={'id':id})
  else:
    return Response(data={'message': 'you are logged out'}, status=status.HTTP_404_NOT_FOUND)