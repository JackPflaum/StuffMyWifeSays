from django.db import models
from django.template.defaultfilters import slugify
import os
from django.conf import settings
from django.core.files import File
import uuid
from phonenumber_field.modelfields import PhoneNumberField

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
    """Store users shopping cart session that is created when the user adds an item to the shopping cart"""

    STATUS_CHOICES = [('open', 'Open'), ('closed', 'Closed'), ('abandoned', 'Abandoned')]

    # a new uuid (unique identifier) value is generated using the uuid4() function each time a new object is created
    cart_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
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
    """stores product details such as size and quantity for each item in the shopping cart"""

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


class Order(models.Model):
    """stores customers order details and address"""

    STATUS_CHOICES = [('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')]

    # order information
    order_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15, default='pending')
    date_ordered = models.DateTimeField(auto_now_add=True)

    # customer information
    email = models.EmailField()
    phone = PhoneNumberField(region='AU')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    state = models.CharField(max_length=20)
    post_code = models.CharField(max_length=20)

    def __str__(self):
        return f'Order No.# {self.order_number}'
    
    def save(self, *args, **kwargs):
        # create an order_number if one has not been created
        if not self.order_number:
            self.order_number = uuid.uuid4
        super().save(*args, **kwargs)
    
    def calculate_total_price(self):
        """calculate total price of the order from relationship with OrderItem model"""
        self.total_price = 0

        # using related_name 'order_items' from OrderItem order field.
        for order_item in self.order_items.all():
            self.total_price += order_item.quantity * order_item.price
        self.save()


class OrderItem(models.Model):
    """stores individual product details for customer's order"""

    SHIRT_SIZE_CHOICES = [('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('xlarge', 'XLarge')]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_products')

    # include price because you want to record the price of the item at that time.
    # the product price may change due to discount or something else.
    price = models.DecimalField(max_digits=8, decimal_places=2) 
    quantity = models.PositiveIntegerField(default=1)
    tshirt_size = models.CharField(max_length=15, choices=SHIRT_SIZE_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # get and save the current product price as of ordering.
        # use related_name to access product model and 
        current_price = self.product.price
        self.price = current_price
        super().save(*args, **kwargs)