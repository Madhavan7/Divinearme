from django.test import Client, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from search.models.user_profile import UserModel
from search.models.temple import temple
from search.models.event import event
import json as json

class UserViewSetTestCase(TransactionTestCase):
  def setUp(self) -> None:
    #create a user to compare with
    self.test_user = User.objects.create_user(username="test1", password="test1")
    self.test_user_model = UserModel.objects.create(user=self.test_user, biography = "test 1")

    #create another user, we will use this to test retrieval
    self.test_user3 = User.objects.create_user(username="test3", password="test3")
    self.test_user3_model = UserModel.objects.create(user=self.test_user3, biography = "test 3")

    #creating a temple to test list
    self.temple = temple.objects.create(name="list_temple", temple_location="kerala", private=True)
    self.temple.temple_members.add(self.test_user_model)
    self.temple.save()
    self.event = event.objects.create(name="welcome event", religious_establishment=self.temple, private = True)
    self.event.save()
    return super().setUp()
  
  def test_create_user(self):
    client = Client()
    url = reverse('user-create')
    #cannot create the account
    response1 = client.post(url, data={"username":"test1", "password":"test1"})
    #can create the account
    response2 = client.post(url, data={"username":"test2", "password":"test1"})
    self.assertEquals(response1.status_code, 400)
    self.assertEquals(response2.status_code, 201)
    test_user = User.objects.get(username="test1")
    assert(test_user is not None)
    assert(UserModel.objects.filter(user=test_user).exists())
  
  def login(self, user:str, password:str):
    client = Client()
    login_url = reverse('token_obtain_pair')
    token = client.post(login_url, data={"username":user, "password":password}).data['access']
    return token, client
  
  def test_retrieve_user_correct(self):
    """
    Tests the case where a user logs in to see his/her account
    """
    token, client = self.login("test3", "test3")
    assert(token is not None)
    assert(client is not None)
    url = reverse('user-detail', kwargs={'pk':str(self.test_user3_model.id)})
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert(response.data['username'] == 'test3')
    assert(response.data['include'] == ['temples', 'events', 'temple_invitations', 'event_invitations', 'temple_requests', 'event_requests'])
  
  def test_retrieve_user_wrong(self):
    """
    Tests the case where a user logs in to see an account thats not his/hers
    """
    token, client = self.login("test1", "test1")
    assert(token is not None)
    assert(client is not None)
    url = reverse('user-detail', kwargs={'pk':str(self.test_user3_model.id)})
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    assert(response.data['username'] == 'test3')
    assert(response.data['include'] == [])
  
  def test_list_temple(self):
    """we are going to test whether a user can view the list of users in a temple"""
    token, client = self.login("test1", "test1")
    url = reverse('temple-user-list', kwargs={'temple_pk':self.temple.id})
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    self.assertEquals(response.status_code, 200)

    #testing the case where client is not a member
    token3, client3 = self.login("test3", "test3")
    response = client3.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'})
    self.assertEquals(response.status_code, 401)

    #same user should be able to view the list even though he is not a member
    self.temple.private = False
    self.temple.save()
    response = client3.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'})
    self.assertEquals(response.status_code, 200)
  
  def test_list_temple_requests(self):
    """tests whether admin of the temple can see the requests to join"""
    self.temple.admins.add(self.test_user_model)
    self.temple.requests_to_join.add(self.test_user3_model)
    self.temple.save()
    token, client = self.login("test1", "test1")
    url = reverse('temple-user-list', kwargs={'temple_pk':self.temple.id})
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, QUERY_STRING='join_request=1')
    #below counts the number of users
    self.assertEquals(response.data['count'],1)
    self.assertEquals(response.data['results'][0]['username'],"test3")

    #test3 must not have access to the temples requested users
    token3, client3 = self.login("test3", "test3")
    url3 = reverse('temple-user-list', kwargs={'temple_pk':self.temple.id})
    response3 = client3.get(url3, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'}, QUERY_STRING='join_request=1')
    self.assertEquals(response3.status_code, 401)

  def test_list_event(self):
    self.event.event_members.add(self.test_user3_model)
    self.event.save()
    
    #should be able to view since he is a temple member
    token, client = self.login("test1", "test1")
    url = reverse('event-user-list', kwargs={'event_pk':self.event.id})
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    self.assertEquals(response.status_code, 200)

    token3, client3 = self.login("test3", "test3")
    url3 = reverse('event-user-list', kwargs={'event_pk':self.event.id})
    response3 = client3.get(url3, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'})
    self.assertEquals(response3.status_code, 200)

    self.event.event_members.remove(self.test_user3_model)
    self.event.save()
    response4 = client3.get(url3, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'})
    self.assertEquals(response4.status_code, 401)

  def test_event_list_request(self):
    token3, client3 = self.login("test3", "test3")
    url3 = reverse('event-user-list', kwargs={'event_pk':self.event.id})
    response = client3.get(url3, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'}, QUERY_STRING='join_request=1')
    self.assertEquals(response.status_code, 401)
    
    #Still he shoudnt be able to see it since he is not an admin
    self.event.event_members.add(self.test_user3_model)
    self.event.save()
    response = client3.get(url3, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'}, QUERY_STRING='join_request=1')
    self.assertEquals(response.status_code, 401)

    #test1 is an admin so he can view 
    self.temple.admins.add(self.test_user_model)
    self.temple.save()
    token, client = self.login("test1", "test1")
    url = reverse('event-user-list', kwargs={'event_pk':self.event.id})
    response = client.get(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, QUERY_STRING='join_request=1')
    self.assertEquals(response.status_code, 200)

  def test_put_wrong_user(self):
    test_user3 = User.objects.get(username="test3")
    token, client = self.login("test1", "test1")
    url = reverse('user-detail', kwargs={"pk": self.test_user3_model.id})
    response = client.put(url,json.dumps({"password": "3"}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEquals(response.status_code, 403)
    assert(User.check_password(test_user3, "test3"))
  
  def test_put_right_user(self):
    token, client = self.login("test1", "test1")
    url = reverse('user-detail', kwargs={"pk": self.test_user_model.id})
    response = client.put(url,json.dumps({"username":"1","password":"1"}),**{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEquals(response.status_code, 200)
    assert(not User.objects.filter(username="test1").exists())
    test_user = User.objects.get(username="1")
    assert(User.check_password(test_user, "1"))

  def test_destroy_wrong_user(self):
    token, client = self.login("test1", "test1")
    url = reverse('user-destroy', kwargs={"pk": self.test_user3_model.id})
    response = client.delete(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEquals(response.status_code, 403)

  def test_destroy_right_user(self):
    token, client = self.login("test1", "test1")
    url = reverse('user-destroy', kwargs={"pk": self.test_user_model.id})
    response = client.delete(url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'}, content_type='application/json')
    self.assertEquals(response.status_code, 204)
    assert(not User.objects.filter(username = "test1").exists())


