from django.contrib import admin
from .models.membership import membership
from .models.event import event
from .models.invitation import temple_invitation
from .models.invitation import event_invitation
from .models.location import location
from .models.temple import temple
from .models.posts import post
from .models.posts import comment
from .models.posts import commentReply
# Register your models here.
admin.site.register(membership)
admin.site.register(event)
admin.site.register(temple)
admin.site.register(temple_invitation)
admin.site.register(event_invitation)
admin.site.register(post)
admin.site.register(comment)
admin.site.register(commentReply)
admin.site.register(location)