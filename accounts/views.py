
from django.contrib import messages, auth

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from grid.models import Grid_data
User = get_user_model()
from django.shortcuts import render, redirect
from django.contrib import auth

from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages  # Import the messages module
from django.contrib.auth.decorators import login_required

def CustomLoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:  # Check if authentication is successful
            auth.login(request, user)

            if user.username == 'user1':
                return redirect('accounts:index')
            elif user.username == 'user2':
                return redirect('accounts:index')
            elif user.username == 'admin':
                return redirect('grid:index') 
            # Replace 'view_grid.html' with the actual URL for user1's dashboard
            # Add similar checks for other user types and their respective dashboard URLs

        else:
            messages.error(request, 'Invalid credentials')  # Use messages.error instead of messages.info for an error message

    return render(request, 'auth/login.html')
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def index(request):
    companys= Grid_data.objects.values('company').distinct()
    context = {
        'companys':companys
    }
    return render(request, 'view_grid.html', context)

from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def logout(request):
    auth.logout(request)
    return redirect('accounts:login')