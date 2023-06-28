from django.db import models
from django.template.defaultfilters import slugify

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
    image = models.ImageField(upload_to='product_images/', default='static/images/Image_not_available.png')
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        """auto-populate slug field"""
        if not self.slug:
            self.slug = slugify(self.product_name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name