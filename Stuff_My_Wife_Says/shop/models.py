from django.db import models
from django.template.defaultfilters import slugify
import os
from django.conf import settings
from django.core.files import File
import uuid

class Category(models.Model):
    """Category model stores information on the categories of products that are sold"""
    CATEGORY_CHOICES = [
        ('T-Shirts', 'T-Shirts'),
        ('Mugs', 'Mugs'),
    ]
    
    category_name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        """auto-populate slug field"""
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    """Product model stores information on the products that are sold"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_name = models.CharField(max_length=255)

    # include price because you want to record the price of the item at that time. the product price may change due to discount or something else.
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', default='product_images/Image_not_available.png')
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        """auto-populate slug field"""
        # auto-populate slug field
        if not self.slug:
            self.slug = slugify(self.product_name)

        # sets the image to the default image when no image is selected during model creation.
        # avoids multiple copies of the default image.
        if not self.image:
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'product_images/Image_not_available.png')
            with open(default_image_path, 'rb') as f:
                self.image.save('Image_not_available.png', File(f), save=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name


class ShoppingCartSession(models.Model):

    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed'), ('abandoned', 'Abandoned')]

    # a new uuid (unique identifier) value is generated using the uuid4() function each time a new object is created
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    modified = models.DateTimeField(auto_now=True)

    def order_total_price(self):
        """Calculates the total price of the order. It uses the cart_items related name from ShoppingCartItem
        to get the query_set of cart items. It than iterate over each item and calculate the specific
        items total price based on it's quantity and price."""
        total_price = sum(item.calculate_cart_item_price() for item in self.cart_items.all())
        return total_price

class ShoppingCartItem(models.Model):

    SHIRT_SIZE_CHOICES = [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('xlarge', 'XLarge')]

    cart = models.ForeignKey(ShoppingCartSession, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    tshirt_size = models.CharField(max_length=15, choices=SHIRT_SIZE_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def calculate_cart_item_price(self):
        """calculate the total price of the cart item based on the quantity ordered"""
        return self.quantity * self.product.price



