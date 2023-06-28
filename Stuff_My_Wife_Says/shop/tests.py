from django.test import TestCase
from django.urls import reverse, resolve
from shop.views import HomePageView, AboutView

class HomeTests(TestCase):
    """Testing the home view"""

    def test_home_view_success_status(self):
        url = reverse('home') # get URL for 'home' url pattern
        response = self.client.get(url) # send GET request to url
        self.assertEqual(response.status_code, 200) # assert the response status code is 200
    
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        # assert that the resolved view function matches the expected view class
        self.assertEqual(view.func.view_class, HomePageView)


class AboutTest(TestCase):
    """About Us page tests"""

    def test_about_view_success_status(self):
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_about_url_resolves_about_view(self):
        view = resolve('/about/')
        self.assertEqual(view.func.view_class, AboutView)
