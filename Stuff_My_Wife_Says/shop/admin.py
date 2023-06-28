from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'product_name', 'price', 'image', 'slug']

    def category_name(self, obj):
        """retrieve category_name from Category object for displaying in the Product model interface"""
        # obj parameter represents an instance of Product model.
        # obj.category retrieves the related 'Category' object associated with the Product instance.
        # can therefore access category_name field.
        return obj.category.category_name

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
