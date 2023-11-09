from django.shortcuts import render

# Create your views here.
def view_grid(request):
    return render(request,'view_grid.html')