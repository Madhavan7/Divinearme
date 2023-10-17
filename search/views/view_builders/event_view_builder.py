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
        response['include'] = []
        pass
    
class EventNormalView(EventViewBuilder):
    def build(self, event, response):
        super().build(event, response)
        response['include'].append('event_members')
    
class EventAdminView(EventViewBuilder):
    def build(self, event, response):
        super().build(event, response)
        response['include'].extend(['event_members', 'invited_users', 'requested_users'])
        
class EventGuestView(EventViewBuilder):
    def build(self, event, response):
        return super().build(event, response)