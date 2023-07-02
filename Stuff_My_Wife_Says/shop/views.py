from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Category, Product, ShoppingCartSession, ShoppingCartItem
from .forms import AddProductToCartForm
from django.contrib.sessions.models import Session
import uuid


class HomePageView(TemplateView):
    """home page view"""
    template_name = 'home.html'


class CategoryView(TemplateView):
    template_name = 'category.html'


def products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category).order_by('price')
    return render(request, 'products.html', {'category': category,'products': products})


def product_details(request, pk):
    """diplay product information and form for product quantity and size"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = AddProductToCartForm(request.POST)
        if form.is_valid():
            cart_uuid = request.session.get('cart_uuid')
            if cart_uuid is not None:
                try:
                    #get shoppingcartsession obj
                    # get or filter ShoppingCartItem obj by shoppingcartsession
                    # if exists overwrite details or create obj and add with form details.
                    # if exists, then adjust template so it lets the user know if they have
                    # added to shoppingcart and if they want to change details.
                    pass
                except ShoppingCartSession.DoesNotExist:
                    pass
            else:
                # create uuid and store it under 'cart_uuid' in 'request.session' dictionary.
                cart_uuid = uuid.uuid4()
                request.session['cart_uuid'] = str(cart_uuid)

                # create 'ShoppingCartSession' obj and save session uuid to it.
                cart = ShoppingCartSession()
                cart.cart_uuid = cart_uuid
                cart.save()
                
                # create 'ShoppingCartItem' obj and save form details to it.
                cart_item = ShoppingCartItem(cart=cart)
                cart_item.product = Product.object.get(pk=pk)
                cart_item.quantity = form.cleaned_data['quantity']
                cart_item.size = form.cleaned_data['size']
                # cart_item.save()
                
                # return back to products page
                return redirect('products', pk=product.category.pk)
    else:
        form = AddProductToCartForm()
        context = {'form': form, 'product': product}
        return render(request, 'product_details.html', context)
        

class AboutView(TemplateView):
    """information about the company"""
    template_name = 'about_us.html'


def contact(request):
    return render(request, 'contact.html', {})


def shopping_cart(request):
    """displays the users current shopping cart session if it exists."""
    # if cart_uuid exists in session then look for cart_uuid in ShoppingCartSession object.
    # render shopping_html html otherwise render no_cart html if no object exists.
    cart_uuid = request.session.get('cart_uuid')
    if cart_uuid is not None:
        try:
            shopping_cart = ShoppingCartSession.objects.get(cart_uuid=cart_uuid)
            return render(request, 'hopping_cart.html', {'shopping_cart': shopping_cart})
        except ShoppingCartSession.DoesNotExist:
            return render(request, 'no_shopping_cart.html', {})
    else:
        return render(request, 'no_shopping_cart.html', {})
