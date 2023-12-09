from django.test import TransactionTestCase, Client
from django.urls import reverse
import json
from django.contrib.auth.models import User
from search.models.user_profile import UserModel
from search.models.temple import temple
from search.models.event import event
from search.models.posts import TemplePost, EventPost

class TestPostViewSet(TransactionTestCase):
  def setUp(self) -> None:
    #to test temple post
    self.temple1 = temple.objects.create(name="temp1", temple_location="251 Jarvis St, Toronto, ON, CA", city = "Toronto", country="Canada")
    self.temple1.save()

    #to test event post
    self.event1 = event.objects.create(name="inaugration", religious_establishment= self.temple1)
    self.event1.save()

    #creating some users
    #this user will comment on the temple
    self.user1 = User.objects.create(username = "madhav")
    self.user1.set_password("sat.chit.anand")
    self.user1.save()
    self.user_model1 = UserModel.objects.create(user=self.user1)
    self.user_model1.save()

    #this user will comment on event
    self.user2 = User.objects.create(username = "meenakshi")
    self.user2.set_password("sat.chit.anand")
    self.user2.save()
    self.user_model2 = UserModel.objects.create(user=self.user2)
    self.user_model2.save()

    #user not in temple or event
    self.user3 = User.objects.create(username = "arya")
    self.user3.set_password("sat.chit.anand")
    self.user3.save()
    self.user_model3 = UserModel.objects.create(user=self.user3)
    self.user_model3.save()

    self.temple1.temple_members.add(self.user_model1)
    self.temple1.private = True
    self.event1.event_members.add(self.user_model2)

    self.event1.private = True
    self.event1.save()
    self.temple1.save()

    return super().setUp()

  def login(self, user:str, password:str):
    client = Client()
    login_url = reverse('token_obtain_pair')
    token = client.post(login_url, data=json.dumps({"username":user, "password":password}),content_type='application/json').data['access']
    return token, client
  
  def test_post_create_retrieve_update(self):
    token1, client1 = self.login("madhav", "sat.chit.anand")
    token2, client2 = self.login("meenakshi", "sat.chit.anand")
    token3, client3 = self.login("arya", "sat.chit.anand")

    url = reverse('temple-post-create', kwargs={'temple_pk':self.temple1.id})
    url2 = reverse('event-post-create', kwargs = {'event_pk':self.event1.id})

    #arya tries to create a post
    response = client3.post(url,json.dumps({'title':'just a stranger', 'text':'nothing just a stranger'}),**{'HTTP_AUTHORIZATION': f'Bearer {token3}'},content_type='application/json')
    self.assertEqual(response.status_code, 401)
    
    #frustrated by his attempt, he tries to post in the event
    response = client3.post(url2,json.dumps({'title':'just a stranger', 'text':'nothing just a stranger'}),**{'HTTP_AUTHORIZATION': f'Bearer {token3}'},content_type='application/json')
    self.assertEqual(response.status_code, 401)

    #madhav tries to post
    response1 = client1.post(url, json.dumps({'title':'not just a stranger', 'text':'not just a stranger, I am admin'}), **{'HTTP_AUTHORIZATION': f'Bearer {token1}'}, content_type='application/json')
    self.assertEqual(response1.status_code, 201)
    
    #meenakshi tries to post
    response2 = client2.post(url2, json.dumps({'title':'I belong to this event', 'text':'first'}), **{'HTTP_AUTHORIZATION': f'Bearer {token2}'}, content_type='application/json')
    self.assertEqual(response2.status_code, 201)

    #madhav should be able to post in the event as he is part of the temple
    response = client1.post(url2,json.dumps({'title':'just a stranger', 'text':'nothing just a stranger'}),**{'HTTP_AUTHORIZATION': f'Bearer {token1}'},content_type='application/json')
    self.assertEqual(response.status_code, 201)

    #Meenakshi cannot post in temple
    response = client3.post(url,json.dumps({'title':'just a stranger', 'text':'nothing just a stranger'}),**{'HTTP_AUTHORIZATION': f'Bearer {token2}'},content_type='application/json')
    self.assertEqual(response.status_code, 401)

    retrieve_url = reverse("temple-post-detail", kwargs={'temple_pk': self.temple1.id, 'pk':1})
    retrieve_url_event = reverse("event-post-detail", kwargs={'event_pk': self.event1.id, 'pk':2})

    #testing get for the temple posts
    response = client1.get(retrieve_url, **{'HTTP_AUTHORIZATION': f'Bearer {token1}'},content_type='application/json')
    self.assertEqual(response.status_code, 200)

    response = client2.get(retrieve_url, **{'HTTP_AUTHORIZATION': f'Bearer {token2}'},content_type='application/json')
    self.assertEqual(response.status_code, 401)

    response = client2.get(retrieve_url, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'},content_type='application/json')
    self.assertEqual(response.status_code, 401)

    #testing get for the event posts
    response = client1.get(retrieve_url_event, **{'HTTP_AUTHORIZATION': f'Bearer {token1}'},content_type='application/json')
    self.assertEqual(response.status_code, 200)

    response = client2.get(retrieve_url_event, **{'HTTP_AUTHORIZATION': f'Bearer {token2}'},content_type='application/json')
    self.assertEqual(response.status_code, 200)

    response = client2.get(retrieve_url_event, **{'HTTP_AUTHORIZATION': f'Bearer {token3}'},content_type='application/json')
    self.assertEqual(response.status_code, 401)

    list_url = reverse("temple-post-list", kwargs={"temple_pk": self.temple1.id})
    list_url_event = reverse("event-post-list", kwargs={"event_pk":self.event1.id})



