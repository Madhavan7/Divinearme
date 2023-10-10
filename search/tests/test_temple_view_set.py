from django.test import TestCase
from django.contrib.auth.models import User

class TempleViewTest(TestCase):
    def setUp(self) -> None:
        admin = User.objects.get(username = "madhavgopakumar")[0]
        member = User.objects.get(username = "roopa-nair")[0]
        non_member = User.objects.get(username = "gopi-nair")[0]
        return super().setUp()