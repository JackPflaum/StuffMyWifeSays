from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Category, Product, ShoppingCartSession, ShoppingCartItem, Order, OrderItem
from .forms import AddTShirtToCartForm, AddMugToCartForm, PaymentForm, CustomerDetailsForm
from django.contrib.sessions.models import Session
import uuid
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages


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
    shopping_cart_item = get_object_or_404(ShoppingCartItem, pk=pk)
    shopping_cart_item.delete()

    return redirect('shopping_cart')


def update_quantity(request):
    """updates the ShoppingCartItem model based on the user increasing or reducing
    the quantity of an item"""
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity =int(request.POST.get('quantity'))
        
        shopping_cart_item = get_object_or_404(ShoppingCartItem, pk=item_id)
        shopping_cart_item.quantity = quantity
        shopping_cart_item.save()
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    

def checkout(request, cart_uuid):
    """checkout for getting user address and payment details"""
    # forms for customer payment and contact information
    payment_form = PaymentForm(request.POST or None)
    customer_details_form = CustomerDetailsForm(request.POST or None)

    context = {'payment_form': payment_form, 'customer_details_form': customer_details_form}

    if request.method == 'POST':

        # process form data if valid
        if payment_form.is_valid() and customer_details_form.is_valid():
            # create Order object
            order = Order()
            # add form data to order fields
            # customer information
            order.first_name = customer_details_form.cleaned_data['first_name']
            order.last_name = customer_details_form.cleaned_data['last_name']
            order.email = customer_details_form.cleaned_data['email']
            order.phone = customer_details_form.cleaned_data['phone']
            order.address = customer_details_form.cleaned_data['address']
            order.suburb = customer_details_form.cleaned_data['suburb']
            order.state = customer_details_form.cleaned_data['state']
            order.post_code = customer_details_form.cleaned_data['post_code']

            # create uuid number for order_number field
            order_number = uuid.uuid4()
            order.order_number = order_number
            order.save()

            # get customers shopping cart and transfer item information to OrderItem model.
            shopping_cart = get_object_or_404(ShoppingCartSession, cart_uuid=cart_uuid)
            shopping_cart_items = ShoppingCartItem.objects.filter(cart=shopping_cart)
            # create OrderItem objects for each item in the order
            for item in shopping_cart_items:
                order_item = OrderItem()
                order_item.order = order
                order_item.product = item.product
                order_item.quantity = item.quantity
                order_item.tshirt_size = item.tshirt_size or ''
                order_item.save()
                
            # get the total price of the order from product quantity and price
            order.total_price = order.calculate_total_price()
            order.save()
                
            # NOTE: do nothing with payment details since this is just a mock payment system.

            # update ShoppingCartSession status from 'open' to 'closed'
            shopping_cart.status = 'closed'
            shopping_cart.save()

            return redirect('purchase_confirmed', order_number=order_number)
        else:
            # if the forms are not valid, re-render the checkout page with the forms and error messages
            messages.error(request, 'Error: Please correct the form errors.')
            return render(request, 'checkout.html', context)
    else:
        return render(request, 'checkout.html', context)


def purchase_confirmed(request, order_number):
    """purchase confirmation receipt appears on screen with customer's order number"""

    # Order has been confirmed, and therfore can delete customer cart session
    if 'cart_uuid' in request.session:
        del request.session['cart_uuid']
    
    order = get_object_or_404(Order, order_number=order_number)
    context = {'order': order}
    return render(request, 'purchase_confirmed.html', context)
