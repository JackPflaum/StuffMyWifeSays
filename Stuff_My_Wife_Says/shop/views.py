from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Category, Product, ShoppingCartSession, ShoppingCartItem
from .forms import AddTShirtToCartForm, AddMugToCartForm
from django.contrib.sessions.models import Session
import uuid
from django.core.paginator import Paginator



class HomePageView(TemplateView):
    """home page view"""
    template_name = 'home.html'


class CategoryView(TemplateView):
    template_name = 'category.html'


def products(request, pk):
    """products page to display products available to the customer in card format."""
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category).order_by('price')

    # create Paginator object and pass query_set and number of items per page
    paginator = Paginator(products, 2)

    # get the current page number from the request's query paramaters
    page_number = request.GET.get('page')

    # get the page object for the current page
    # get_page() method will return last page if page_number is outside range or
    # first page if page_number isn't a valid number.
    page_obj_products = paginator.get_page(page_number)

    # pass page object into context dictionary
    context = {'products': page_obj_products}

    return render(request, 'products.html', context)


def product_details(request, pk):
    """diplay product information and allow users to add product to cart."""
    product = get_object_or_404(Product, pk=pk)

    # retrieve the form for the corresponding product.
    # get the tshirt form, otherwise get the mug form.
    if product.category.category_name == 'T-Shirts':
        form = AddTShirtToCartForm(request.POST or None)
    else:
        form = AddMugToCartForm(request.POST or None)

    # handle form submission data
    if request.method == 'POST' and form.is_valid():
            cart_uuid = request.session.get('cart_uuid')
            
            # if the user has a cart_uuid than get ShoppingCartSession and add item to cart
            if cart_uuid is not None:
                try:
                    # get users shopping cart session, create shopping cart item and add form data
                    cart = ShoppingCartSession.objects.get(cart_uuid=cart_uuid)
                    cart_item = ShoppingCartItem(cart=cart)
                    cart_item.product = product
                    cart_item.quantity = form.cleaned_data['quantity']

                    # check if form has size field for T-shirts
                    if 'size' in form.fields:
                        cart_item.tshirt_size = form.cleaned_data['size']
                    cart_item.save()

                    return redirect('products', pk=product.category.pk)
                    
                except ShoppingCartSession.DoesNotExist:
                    pass
            else:
                # if the user doesn't have a cart session than
                # create uuid and store it under 'cart_uuid' in 'request.session' dictionary.
                cart_uuid = uuid.uuid4()
                request.session['cart_uuid'] = str(cart_uuid)

                # create 'ShoppingCartSession' obj and save session uuid to it.
                cart = ShoppingCartSession()
                cart.cart_uuid = cart_uuid
                cart.save()
                
                # create 'ShoppingCartItem' obj and save form details to it.
                cart_item = ShoppingCartItem(cart=cart)
                cart_item.product = product
                cart_item.quantity = form.cleaned_data['quantity']

                # check if form has size field for T-shirts
                if 'size' in form.fields:
                    cart_item.tshirt_size = form.cleaned_data['size']
                cart_item.save()
                
                # return back to products page
                return redirect('products', pk=product.category.pk)
    else:        
        context = {'form': form, 'product': product}
        return render(request, 'product_details.html', context)
        

class AboutView(TemplateView):
    """information about the company"""
    template_name = 'about_us.html'


def contact(request):
    return render(request, 'contact.html', {})


def shopping_cart(request):
    """displays the users current shopping cart session if it exists."""
    # if cart_uuid exists in session then look for cart_uuid in ShoppingCartSession object
    # and then get shopping cart items.
    # render shopping_html html otherwise render no_cart html if no object exists.
    cart_uuid = request.session.get('cart_uuid')
    if cart_uuid is not None:
        try:
            shopping_cart = ShoppingCartSession.objects.get(cart_uuid=cart_uuid)
            shopping_cart_items = ShoppingCartItem.objects.filter(cart=shopping_cart)

            return render(request, 'shopping_cart.html', {'shopping_cart_items': shopping_cart_items,
                                                          'shopping_cart': shopping_cart})
        except ShoppingCartSession.DoesNotExist:
            return render(request, 'no_shopping_cart.html', {})
    else:
        return render(request, 'no_shopping_cart.html', {})


def remove_item(request, pk):
    """removes item from shopping cart"""
    cart_uuid = request.session['cart_uuid']
    shopping_cart = ShoppingCartSession.objects.get(cart_uuid=cart_uuid)
    shopping_cart_item = ShoppingCartItem.objects.get(pk=pk)
    shopping_cart_item.delete()

    return redirect('shopping_cart')


def update_shopping_cart(request):
    """updates shopping cart with new total price based on the user increasing or reducing
    the quantity of an item"""
    pass

def checkout(request):
    pass
