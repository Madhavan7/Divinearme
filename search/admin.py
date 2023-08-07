from django.contrib import admin
from .models.membership import membership
from .models.event import event
from .models.invitation import TempleInvitation
from .models.invitation import EventInvitation
from .models.location import location
from .models.temple import temple
from .models.posts import post
from .models.posts import TemplePost
from .models.posts import EventPost
from .models.posts import comment
from .models.posts import CommentReply
from .models.user_profile import UserModel
# Register your models here.
admin.site.register(membership)
admin.site.register(event)
admin.site.register(temple)
admin.site.register(TempleInvitation)
admin.site.register(EventInvitation)
admin.site.register(post)
admin.site.register(comment)
admin.site.register(CommentReply)
admin.site.register(location)
admin.site.register(TemplePost)
admin.site.register(EventPost)
admin.site.register(UserModel)