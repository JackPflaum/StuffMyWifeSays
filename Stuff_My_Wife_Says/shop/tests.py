from django.test import TestCase
from django.urls import reverse, resolve
from shop.views import HomePageView, AboutView
from .models import Category, Product
from django.core.paginator import Paginator

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


class ProductsTest(TestCase):
    """Products page tests"""

    def setUp(self):
        # create test categories
        self.category_mug = Category.objects.create(category_name='Mugs')
        self.category_tshirt = Category.objects.create(category_name='T-shirts')
        
        # create test mug products
        self.product1 = Product.objects.create(category=self.category_mug, product_name='This is a mug', price=20.55)
        self.product2 = Product.objects.create(category=self.category_mug, product_name='This is another mug', price=19.95)
        self.product3 = Product.objects.create(category=self.category_mug, product_name='This is also mug', price=10.75)
        
        # create test tshirt products
        self.product4 = Product.objects.create(category=self.category_tshirt, product_name='This is a tshirt', price=35.95)
        self.product5 = Product.objects.create(category=self.category_tshirt, product_name='This is another tshirt', price=39.5)

        # sort products based on price in ascending order because 'products' view orders_by('price')
        self.mug_products = [self.product1, self.product2, self.product3] 
        # takes product object as input and returns it's price. The sort method uses this value to arrage
        # objects in 'mug_products'.
        self.mug_products.sort(key=lambda product: product.price) 

    def test_products_pagination(self):
        """testing pagination in products page"""

        url = reverse('products', args=[self.category_mug.pk])
        response = self.client.get(url)

        # assert response status is 200
        self.assertEqual(response.status_code, 200)

        # assert 2 mug products displayed on the first page 
        self.assertEqual(len(response.context['products']), 2)

        # get the Paginator object from the response's context
        paginator_page1 = response.context['products'].paginator

        # assert the paginator has the correct number of pages
        # 3 mug products, 2 per page, therefore 2 pages to display the products
        self.assertEqual(paginator_page1.num_pages, 2)

        # assert product1 and product2 appear on the first page
        self.assertIn(self.mug_products[0], [product for product in response.context['products']])
        self.assertIn(self.mug_products[1], [product for product in response.context['products']])

        # assert product3 appears on the second page
        response = self.client.get(url + '?page=2')    # get 2nd page
        self.assertEqual(response.status_code, 200)    # assert status OK
        self.assertIn(self.mug_products[2], [product for product in response.context['products']])
