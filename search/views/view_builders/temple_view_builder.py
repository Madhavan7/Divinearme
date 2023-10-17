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
    response['include'] = []
    pass

class TempleNormalView(TempleViewBuilder):
  def build(self, temple, response):
    response['include'] = ['events', 'temple_members']

class TempleAdminView(TempleViewBuilder):
  def build(self, temple, response):
    response['include'] = ['events', 'temple_members', 'invited_users', 'requested_users']


class TempleGuestView(TempleViewBuilder):
  def build(self, temple, response):
    super().build(temple, response)
