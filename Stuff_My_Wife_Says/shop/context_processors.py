from .models import Category

# Context processors are functions that add data to the context dictionary of every template.
def navbar_context(request):
    """context for dynamic dropdown menu for Products link"""
    categories = Category.objects.all()
    return {'categories': categories}