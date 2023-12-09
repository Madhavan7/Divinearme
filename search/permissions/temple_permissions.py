from rest_framework.permissions import BasePermission, SAFE_METHODS
from search.models.user_profile import UserModel

class TempleViewPermission(BasePermission):
    message = "Only temple members can view the members"
    
    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "user"):
            return False
        
        u_model = UserModel.objects.get(user = request.user)

        if request.method in SAFE_METHODS:
            #below is faulty because obj.temple_members.all() is a queryset not an object
            u_model = UserModel.objects.get(user = request.user)
            return obj.can_view(u_model)
        else:
            return False

class TemplePostCommentPermission(BasePermission):
    message = "Only temple members can comment"

    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "user"):
            return False
        u_model = UserModel.objects.get(user = request.user)
        return obj.temple_members.all().filter(id =u_model.id).exists()
    
class TempleUpdatePermission(BasePermission):
    message = "only admins can update the info"

    def has_object_permission(self, request, view, obj):
        if not hasattr(request, "user"):
            return False
        u_model = UserModel.objects.get(user = request.user)
        return obj.admins.all().filter(id = u_model.id).exists()