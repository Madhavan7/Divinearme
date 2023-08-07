from rest_framework.permissions import BasePermission, SAFE_METHODS

class TempleViewPermission(BasePermission):
    message = "Only temple members can view the members"
    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "user"):
            return False
        if obj.private and request.method in SAFE_METHODS:
            #below is faulty because obj.temple_members.all() is a queryset not an object
            for temp in obj.temple_members.all():
                if request.user.id == temp.user.id:
                    return True
            return False
        elif not obj.private:
            return request.method in SAFE_METHODS

class TemplePostCommentPermission(BasePermission):
    message = "Only temple members can comment"

    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "user"):
            return False
        for temp in obj.temple_members.all():
            if request.user.id == temp.user.id:
                return True
        return False
    
class TempleUpdatePermission(BasePermission):
    message = "only admins can update the info"

    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "user"):
            return False
        for temp in obj.admins.all():
            if request.user.id == temp.user.id:
                return True
        return False