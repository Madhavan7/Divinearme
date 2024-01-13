from rest_framework.permissions import BasePermission, SAFE_METHODS
from .temple_permissions import *

class EventViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):

        if not hasattr(request, "user"):
            return False
        
        if request.method in SAFE_METHODS:
            u_model = UserModel.objects.get(user = request.user)
            return obj.can_view(u_model)
        else:
            return False

class EventPostCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.private:
            return True
        temple = obj.religious_establishment
        u_model = UserModel.objects.get(user = request.user)
        return TemplePostCommentPermission().has_object_permission(request, view, temple) or obj.event_members.filter(id=u_model.id).exists()

class EventUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        temple = obj.religious_establishment
        return TempleUpdatePermission().has_object_permission(request, view, temple)