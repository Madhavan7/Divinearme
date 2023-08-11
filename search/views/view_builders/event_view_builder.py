from search.permissions.event_permissions import *
from search.serializers.member_serializer import MemberSerializer

class EventViewDirector():
    def __init__(self, event, request) -> None:
        admin = EventUpdatePermission().has_object_permission(request, None, event)
        can_view = EventViewPermission().has_object_permission(request, None, event)
        if admin:
            self._builder = EventAdminView()
        elif can_view:
            self._builder = EventNormalView()
        else:
            self._builder = EventGuestView()
    def build(self, event, response):
        self._builder.build(event, response)

#TODO: complete the below first thing in the morning
class EventViewBuilder():
    def build(self, event, response):
        pass
    
class EventNormalView(EventViewBuilder):
    def build(self, event, response):
        super().build(event, response)
        response['event_members'] = MemberSerializer(event.event_members.all().order_by("user__username")[:5], many = True).data
    
class EventAdminView(EventViewBuilder):
    def build(self, event, response):
        super().build(event, response)
        response['event_members'] = MemberSerializer(event.event_members.all().order_by("user__username")[:5], many = True).data
        response['invited_users'] = MemberSerializer(sorted(event.invited_users.all(), key= lambda x:x.invitations.get(event_invitation__associated_event = event).invite_time)[:5], many = True).data
        response['requested_users'] = MemberSerializer(sorted(event.requests_to_join.all(), key= lambda x:x.invitations.get(event_invitation__associated_event = event).invite_time)[:5], many = True).data
        
class EventGuestView(EventViewBuilder):
    def build(self, event, response):
        return super().build(event, response)