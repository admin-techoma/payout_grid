from django.shortcuts import render

from grid.models import Product

# Create your views here.
def view_grid(request):
    product = Product.objects.all()
    context = {
        'product':product
    }
    return render(request,'view_grid.html',context)