from rest_framework.permissions import BasePermission, SAFE_METHODS
from .temple_permissions import *

class EventViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.private:
          temple = obj.religious_establishment
          return TempleViewPermission().has_object_permission(request, view, temple)
        else:
            return request.method in SAFE_METHODS

class EventPostCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.private:
            return True
        temple = obj.religious_establishment
        return TemplePostCommentPermission().has_object_permission(request, view, temple)

class EventUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        temple = obj.religious_establishment
        return TempleUpdatePermission().has_object_permission(request, view, temple)