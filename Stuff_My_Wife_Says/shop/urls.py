from django.urls import path
from . import views
from shop.views import (HomePageView, AboutView, CategoryView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categories', CategoryView.as_view(), name='categories'),
    path('products/<int:pk>', views.products, name='products'),
    path('product_details/<int:pk>', views.product_details, name='product_details'),
    # path('shopping_cart/<int:pk>', views.shopping_cart, name='shopping_cart'),
    # path('checkout/<int:pk>', views.checkout, name='checkout'),
    # path('purchase_confirmed/<int:pk>', views.purchase_confirmed, name='purchase_confirmed'),
    path('about/', AboutView.as_view(), name='about'),
    # path('contact/', views.contact, name='contact'),
]

# adding media URL pattern and configuration for serving media files during development.
# static() dynamically adds the media URL pattern to the urlpatterns.
# it maps MEDIA_URL to MEDIA_ROOT and tells Django to serve media files from the MEDIA_ROOT directory.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
