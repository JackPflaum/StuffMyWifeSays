from django.contrib import admin
from .models import Category, Product, ShoppingCartSession, ShoppingCartItem, Order, OrderItem

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


class ShoppingCartSessionAdmin(admin.ModelAdmin):
    list_display = ['cart_uuid', 'created_at', 'status', 'modified']


class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ['cart_uuid', 'product', 'quantity', 'tshirt_size', 'created_at', 'modified_at']

    def cart_uuid(self, obj):
        """retrieve cart_uuid connected to product item"""
        return obj.cart.cart_uuid


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'total_price', 'status', 'date_ordered']


class OrderItemAdmin(admin.ModelAdmin):
    # TODO: Need to add order number and product
    list_display = ['order_number', 'price', 'quantity']

    def order_number(self, obj):
        """retrieve order_number connected to order item"""
        return obj.order.order_number


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCartSession, ShoppingCartSessionAdmin)
admin.site.register(ShoppingCartItem, ShoppingCartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
