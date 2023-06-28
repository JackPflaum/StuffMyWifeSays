from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from .models import Category, Product
from .forms import AddProductToCartForm


class HomePageView(TemplateView):
    """home page view"""
    template_name = 'home.html'


class CategoryView(TemplateView):
    template_name = 'category.html'


def products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category).order_by('price')
    return render(request, 'products.html', {'products': products})


def product_details(request, pk):
    """diplay product information and form for product quantity and size"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = AddProductToCartForm(request.POST)
        if form.is_valid():
            # do something
            return redirect('products', pk=pk)
    else:
        form = AddProductToCartForm()
        context = {'form': form, 'product': product}
        return render(request, 'product_details.html', context)
        


class AboutView(TemplateView):
    """information about the company"""
    template_name = 'about_us.html'