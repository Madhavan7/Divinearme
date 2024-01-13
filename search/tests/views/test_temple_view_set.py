from django.test import TransactionTestCase, Client
from django.urls import reverse
from search.models.invitation import TempleInvitation
from search.models.temple import temple
from search.models.user_profile import UserModel
from search.models.event import event
from django.contrib.auth.models import User
from search.models.user_profile import UserModel
import json

class TempleViewSetTest(TransactionTestCase):

  def setUp(self) -> None:
    #Creating user for the user experience
    self.user = User.objects.create(username = "madhav")
    self.user.set_password("sat.chit.anand")
    self.user.save()
    self.user_model = UserModel.objects.create(user=self.user)
    self.user_model.save()

    #Creating user that wont be in the temple, to check in such access in such access
    self.user2 = User.objects.create(username = "meenakshi")
    self.user2.set_password("peace.and.love")
    self.user2.save()
    self.user_model2 = UserModel.objects.create(user=self.user2)
    self.user_model2.save()

    #creating a few temples in various geographic areas 
    #two in toronto
    self.temple1 = temple.objects.create(name="temp1", temple_location="251 Jarvis St, Toronto, ON, CA", city = "Toronto", country="Canada")
    self.temple1.save()
    self.temple2 = temple.objects.create(name="temp2", temple_location="100 Queens Park, Toronto, ON M5S 2C6", city = "Toronto", country="Canada")
    self.temple2.save()

    #two far from Toronto
    self.temple3 = temple.objects.create(name="temp3", temple_location="3800 Queen Mary Rd, Montreal, Quebec H3V 1H6", city = "Montreal", country="Canada")
    self.temple3.save()
    self.temple4 = temple.objects.create(name="temp4", temple_location="300 Sainte Croix Ave, Montreal, Quebec H4N 3K4", city = "Montreal", country="Canada")
    self.temple4.save()
    return super(TempleViewSetTest, self).setUp()
  
  def login(self, user:str, password:str):
    client = Client()
    login_url = reverse('token_obtain_pair')
    token = client.post(login_url, data=json.dumps({"username":user, "password":password}),content_type='application/json').data['access']
    return token, client
  
  def test_create(self):
    token, client = self.login("madhav", "sat.chit.anand")
    url = reverse('temple-create')
    response = client.post(url,json.dumps({"name": "test1"}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEqual(response.status_code, 400)
    response = client.post(url,json.dumps({"name": "test1"}), content_type='application/json')
    self.assertEqual(response.status_code, 401)
    response = client.post(url,json.dumps({"name": "iskcon"}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEqual(response.status_code, 400)
    response = client.post(url, json.dumps({"name": "iskcon", "temple_location": "1440 Don Mills Rd., North York, ON"}), content_type='application/json')
    self.assertEqual(response.status_code, 401)
    response = client.post(url, data=json.dumps({"name": "iskcon", "temple_location": "1440 Don Mills Rd., North York, ON"}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEqual(response.status_code, 201)
    assert(temple.objects.filter(name="iskcon").exists())
    assert(temple.objects.get(name="iskcon").admins.filter(user__username="madhav").exists())

  def test_update(self):
    temple1 = temple.objects.get(id=self.temple1.id)
    # adding admin to the temple
    user_model = UserModel.objects.get(id=self.user_model.id)
    user_model2 = UserModel.objects.get(id = self.user_model2.id)
    temple1.admins.add(user_model)
    temple1.save()
    temple1.refresh_from_db()
    ###########################
    token, client = self.login("madhav", "sat.chit.anand")
    url = reverse('temple-detail', kwargs={'pk': self.temple1.id})
    self.assertTrue(not TempleInvitation.objects.filter(user = user_model2, associated_temple = temple1).exists())
    response = client.put(url,json.dumps({"description":"a nice temple", "temple_members": json.dumps([{"user": self.user_model2.id}])}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    temple1.refresh_from_db()
    self.assertEquals(str(temple1.description),"a nice temple")
    self.assertTrue(TempleInvitation.objects.filter(user = user_model2, associated_temple = temple1).exists())
    response = client.put(url,json.dumps({"description":"a nice temple", "temple_members": json.dumps([{"user": self.user_model2.id}])}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    temple1.refresh_from_db()
    assert(temple1.temple_members.filter(id = self.user_model2.id).exists())
    response = client.put(url,json.dumps({"description":"a nice temple", "admins": json.dumps([{"user": self.user_model2.id}])}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    temple1.refresh_from_db()
    assert(temple1.admins.filter(id = self.user_model2.id).exists())
    token2, client2 = self.login("meenakshi", "peace.and.love")
    response = client2.put(url,json.dumps({"description":"a nice temple", "temple_location": "asdgeg"}),**{'HTTP_AUTHORIZATION': f'Bearer {token2}'}, content_type='application/json')
    temple1.refresh_from_db()
    self.assertEqual(response.status_code, 400)
  
  def test_retrieve_location(self):
    #This test is all thats required for testing retrieve, rest of the tests belong in test_search_strategy
    token, client = self.login("madhav", "sat.chit.anand")
    #get 
    url = reverse('temple-list')
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json', QUERY_STRING='location=89 McGill St, Toronto, ON, CA&radius=10000')
    results = [temp['temple_location'] for temp in response.data['results']]
    assert('3800 Queen Mary Rd, Montreal, Quebec H3V 1H6' not in results)
    assert('300 Sainte Croix Ave, Montreal, Quebec H4N 3K4' not in results)
    assert('251 Jarvis St, Toronto, ON, CA' in results)
    assert("100 Queens Park, Toronto, ON M5S 2C6" in results)
  
  def test_retrieve_user(self):
    token, client = self.login("madhav", "sat.chit.anand")
    url = reverse('user-temple-list', kwargs={'user_pk':self.user_model.id})
    temple1 = temple.objects.get(id=self.temple1.id)
    user_model = UserModel.objects.get(id=self.user_model.id)
    temple1.temple_members.add(user_model)

    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEqual(response.data['results'][0]['name'], 'temp1')
    url2 = reverse('user-temple-list', kwargs={'user_pk':self.user_model2.id})
    response = client.get(url2, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEqual(response.status_code, 401)

  
  def test_get(self):
    temple1 = temple.objects.get(id=self.temple1.id)
    user_model = UserModel.objects.get(id=self.user_model.id)
    temple1.temple_members.add(user_model)
    temple1.save()
    temple1.refresh_from_db()

    url = reverse('temple-detail', kwargs={'pk':self.temple1.id})

    token, client = self.login("madhav", "sat.chit.anand")
    token2, client2 = self.login("meenakshi", "peace.and.love")

    response1 = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    response2 = client2.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token2}'}, content_type='application/json')
    assert('events' in response1.data['include'])
    assert('temple_members' in response1.data['include'])
    assert('invited_users' not in response1.data['include'])
    self.assertNotEqual(response2.data['include'], [])
    temple1.private = True
    temple1.save()
    response2 = client2.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token2}'}, content_type='application/json')
    self.assertEqual(response2.data['include'], [])

    temple1.admins.add(user_model)
    temple1.save()
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    assert('invited_users' in response.data['include'])
  



  