from django.test import TestCase
from django.urls import resolve, reverse

from ..views import PostDetailView

class UrlTest(TestCase):
    def test_HomePage(self):
        response = self.client.get('/')
        print(response)
        
        self.assertEqual(response.status_code, 200)
    def test_post_detail_Page(self):
        url = reverse('post_detail')
        print(f"Resolve: {resolve(url)}")
        
        self.assertEquals(resolve(url).func, PostDetailView)