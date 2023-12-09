from rest_framework.permissions import BasePermission, SAFE_METHODS
from search.models.posts import TemplePost, EventPost
from search.models.temple import temple
from search.models.event import event
from .temple_permissions import *
    
class PostViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            u_model = UserModel.objects.get(user = request.user)
            return obj.can_view(u_model)
        except Exception as e:
            print(e)
            return False
class PostUpdateDeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            u_model = UserModel.objects.get(user=request.user)
            #delete permission is equivalent to update
            return obj.can_delete(u_model)
        except:
            return False