from rest_framework.permissions import BasePermission, SAFE_METHODS
import temple_permissions as temple_perm

class EventViewPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.private:
          temple = obj.religious_establishment
          return temple_perm.TempleViewPermission().has_object_permission(request, view, temple)
        else:
            return request.method in SAFE_METHODS

class EventPostCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.private:
            return True
        temple = obj.religious_establishment
        return temple_perm.TemplePostCommentPermission().has_object_permission(request, view, temple)

class EventUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        temple = obj.religious_establishment
        return temple_perm.TempleUpdatePermission().has_object_permission(request, view, temple)