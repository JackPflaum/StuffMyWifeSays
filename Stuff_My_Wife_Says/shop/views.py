from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Category, Product, ShoppingCartSession
from .forms import AddProductToCartForm
from django.contrib.sessions.models import Session


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
            # do something
            # check is current Session has cart_uuid
            # if yes then add item to current ShoppingCartSession
            # if no then create cart and add cart_uuid to Session
            return redirect('products', pk=pk)
    else:
        form = AddProductToCartForm()
        context = {'form': form, 'product': product}
        return render(request, 'product_details.html', context)
        

class AboutView(TemplateView):
    """information about the company"""
    template_name = 'about_us.html'


def shopping_cart(request):
    # if cart_id (uuid) exists then render shopping_cart html otherwise render no_cart html
    cart_uuid = request.Session['cart_uuid']
    if cart_uuid is not None:
        shopping_cart = ShoppingCartSession.objects.get(cart_uuid=cart_uuid)
        return render(request, 'hopping_cart.html', {'shopping_cart': shopping_cart})
    else:
        return render(request, 'no_shopping_cart.html', {})
