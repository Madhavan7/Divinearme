from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.forms import ValidationError
from search.models.temple import temple
from search.models.event import event
from search.models.user_profile import UserModel
from search.models.invitation import EventInvitation
from search.exceptions.exceptions import InvalidUserException

class EventTest(TransactionTestCase):
  def setUp(self) -> None:
    self.temple = temple.objects.create(name="test", temple_location= "251 Jarvis St, Toronto, ON, CA")
    self.event = event.objects.create(name="inaug event", religious_establishment=self.temple)
    self.users = []

    for i in range(5):
      user = User.objects.create_user(username=str(i), password=str(i))
      user_model = UserModel.objects.create(user=user)
      self.users.append(user_model)

    self.temple.admins.add(self.users[0])
    return super(EventTest, self).setUp()
  
  def test_event_create(self):
    params_temple = [self.temple.placeID, self.temple.lattitude, self.temple.longitude]
    params_event = [self.event.placeID, self.event.lattitude, self.event.longitude]
    #Since event location is not specified
    for i in range(3):
      self.assertEqual(params_temple[i], params_event[i])
    self.event.event_location = "151 Dundas St E, Toronto, ON"
    self.event.save()
    params_event = [self.event.placeID, self.event.lattitude, self.event.longitude]
    for i in range(3):
      self.assertNotEqual(params_temple[i], params_event[i])
    
    try:
      even = event.objects.create(name="test2", event_location= "skjhbwfvjh")
      assert(5==3)
    except ValidationError:
      assert(3==3)
  
  def test_add_remove_members(self):
    self.event.add_members(self.users[0], self.users[1])
    assert(not self.event.event_members.filter(id=self.users[1].id).exists() 
           and EventInvitation.objects.filter(user= self.users[1],associated_event=self.event).exists())
    self.event.add_members(self.users[1], self.users[1])
    assert(self.event.event_members.filter(id=self.users[1].id).exists() 
           and not EventInvitation.objects.filter(user= self.users[1],associated_event=self.event).exists())
    self.event.add_members(self.users[0], self.users[2])
    self.event.add_members(self.users[2], self.users[2])
    try:
      self.event.remove_member(self.users[1], self.users[2])
      assert(5==3)
    except InvalidUserException:
      assert(3==3)
    self.event.remove_member(self.users[0], self.users[2])
    assert(not self.event.event_members.filter(id=self.users[2].id).exists())