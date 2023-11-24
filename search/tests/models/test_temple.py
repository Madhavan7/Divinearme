from django.test import TransactionTestCase, Client
from django.contrib.auth.models import User
from search.models.user_profile import UserModel
from search.models.invitation import TempleInvitation
from search.models.temple import temple
from search.models.event import event
from search.exceptions.exceptions import InvalidUserException
from django.forms import ValidationError

class TempleTest(TransactionTestCase):
  def setUp(self) -> None:
    self.users = []
    for i in range(5):
      user = User.objects.create_user(username=str(i), password=str(i))
      user_model = UserModel.objects.create(user=user)
      self.users.append(user_model)
    self.temple = temple.objects.create(name="test", temple_location="251 Jarvis St, Toronto, ON, CA")
    self.temple.admins.add(self.users[0])
    return super(TempleTest, self).setUp()
  
  def test_temple_create(self):
    try:
      temple.objects.create(name="test3", temple_location = "wergasgwgrq")
      assert(5 == 3)
    except ValidationError:
      assert(3==3)
    
    temp = temple.objects.create(name="test3", temple_location = "61 Carrie Crescent, Brampton, ON, CA", city = "Toronto", country= "Canada")
    self.assertNotEqual(temp.placeID, '') 


  def test_add_remove_member(self):
    self.temple.add_member(self.users[0], self.users[1], "temple_members")
    assert(TempleInvitation.objects.filter(associated_temple=self.temple, user=self.users[1]).exists())
    self.temple.add_member(self.users[1], self.users[1], "temple_members")
    assert(self.temple.temple_members.filter(id=self.users[1].id).exists())
    assert(not TempleInvitation.objects.filter(associated_temple=self.temple, user=self.users[1]).exists())
    try: 
      self.temple.add_member(self.users[1], self.users[2], "temple_members")
      self.temple.add_member(self.users[2], self.users[3], "temple_members")
      assert(5 == 3)
    except InvalidUserException:
      assert(3==3)
    assert(not self.temple.temple_members.filter(id=self.users[2].id).exists())
    assert(not self.temple.temple_members.filter(id=self.users[3].id).exists())
    self.temple.add_member(self.users[0], self.users[1], "admins")
    assert(self.temple.admins.filter(id = self.users[1].id).exists())
    try:
      self.temple.remove_member(self.users[0], self.users[1])
      assert(5==3)
    except InvalidUserException:
      assert(3==3)
    self.temple.add_member(self.users[0], self.users[2], "temple_members")
    self.temple.remove_member(self.users[0], self.users[2])
    self.temple.remove_member(self.users[1], self.users[1])
    assert(not self.temple.temple_members.filter(id=self.users[2].id).exists())
    assert(not self.temple.temple_members.filter(id=self.users[1].id).exists())

  def test_remove_event(self):
    even = event.objects.create(name = "inaug", religious_establishment = self.temple,
                                event_location= "61 Carrie Crescent, Brampton, ON, CA")
    assert(self.temple.events.filter(id = even.id).exists())
    self.temple.remove_event(self.users[0], even)
    assert(not self.temple.events.filter(id=even.id).exists())
