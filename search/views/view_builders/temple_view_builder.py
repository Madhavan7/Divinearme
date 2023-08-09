import search.permissions.temple_permissions as perm
from search.serializers.event_serializer import EventSerializer
from search.serializers.member_serializer import MemberSerializer

class TempleViewDirector():
  def __init__(self, request, temple):
    #init can only return None unfortunately like I suspected
    can_view = perm.TempleViewPermission().has_object_permission(request, None, temple)
    admin = perm.TempleUpdatePermission().has_object_permission(request, None, temple)
    if admin:
      self._builder = TempleAdminView()
    elif can_view:
      self._builder = TempleNormalView()
    else:
      self._builder = TempleGuestView()
  
  def build(self, temple, response):
    self._builder.build(temple, response)


class TempleViewBuilder:
  def build(self, temple, response):
    pass

class TempleNormalView(TempleViewBuilder):
  def build(self, temple, response):
    response['events'] = EventSerializer(temple.events.all().order_by('start_date_time')[:5], many = True).data
    response['temple_members'] = MemberSerializer(temple.temple_members.all().order_by("user__username")[:5], many = True).data

class TempleAdminView(TempleViewBuilder):
  def build(self, temple, response):
    response['events'] = EventSerializer(temple.events.all().order_by('start_date_time')[:5], many = True).data
    response['invited_users'] = MemberSerializer(sorted(temple.invited_users.all(), key= lambda x:x.invitations.get(temple_invitation__associated_temple = temple).invite_time)[:5], many = True).data
    response['requested_users'] = MemberSerializer(sorted(temple.requests_to_join.all(), key= lambda x:x.invitations.get(temple_invitation__associated_temple = temple).invite_time)[:5], many = True).data

class TempleGuestView(TempleViewBuilder):
  def build(self, temple, response):
    super().build(temple, response)
