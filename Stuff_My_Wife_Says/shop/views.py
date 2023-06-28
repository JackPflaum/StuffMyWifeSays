from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Category, Product


class HomePageView(TemplateView):
    """home page view"""
    template_name = 'home.html'


class CategoryView(TemplateView):
    template_name = 'category.html'


def products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category).order_by('')
    return render(request, 'products.html', {'products': products})


class AboutView(TemplateView):
    """information about the company"""
    template_name = 'about_us.html'