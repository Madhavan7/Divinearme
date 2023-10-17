from django.test import SimpleTestCase
from django.urls import reverse, resolve
from search.urls import temple_list

class TestUrls(SimpleTestCase):
    def test_temple_create(self):
        url = reverse('temple-list')
        self.assertEquals(resolve(url).func, temple_list)