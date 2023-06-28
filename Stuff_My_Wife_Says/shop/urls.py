from django.urls import path
from . import views
from shop.views import (HomePageView, AboutView, CategoryView)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('products/<int:pk>', views.products, name='products'),
    # path('product_details/<int:pk>', views.product_details, name='product_details'),
    # path('shopping_cart/<int:pk>', views.shopping_cart, name='shopping_cart'),
    # path('checkout/<int:pk>', views.checkout, name='checkout'),
    # path('purchase_confirmed/<int:pk>', views.purchase_confirmed, name='purchase_confirmed'),
    path('about/', AboutView.as_view(), name='about'),
    # path('contact/', views.contact, name='contact'),
]
