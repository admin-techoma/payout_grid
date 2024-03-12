
from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from grid.models import Employee, Grid_data
User = get_user_model()
from django.shortcuts import redirect,render, get_object_or_404, redirect
from django.contrib import auth
from accounts.forms import CustomPasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages  # Import the messages module
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from accounts.forms import CustomPasswordChangeForm
from django.utils.http import urlsafe_base64_encode
from django.utils.http import  urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def CustomLoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user and Employee.objects.filter(emp_user=user).exists():
            auth.login(request, user)

            employee = Employee.objects.get(emp_user=user)
            if not employee.password_changed:
                print("Password Changed Status:", employee.password_changed)
                print("Redirecting to change_password")
                return redirect('accounts:change_firsttime_password')
            else:
                # Redirect based on user's status
                if user.is_superuser:
                    return redirect('grid:index')
                else:
                    # Redirect based on user's group
                    if user.groups.filter(name='admin').exists():
                        return redirect('grid:index')
                    else:
                        return redirect('accounts:index')
        else:
            messages.error(request, 'Invalid credentials')  # Use messages.error instead of messages.info for an error message

    return render(request, 'auth/login.html')


from django.views.decorators.cache import cache_control


def change_firsttime_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Get the authenticated user
            user = request.user
            
            # Update password_changed flag for the employee
            try:
                employee = Employee.objects.get(emp_user=user)
                employee.password_changed = True
                employee.save()
            except Employee.DoesNotExist:
                # Handle the case where the Employee does not exist for the user
                messages.info(request, 'Employee does not exist')
                return redirect('accounts:login')

            # Save the password change
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:login')  # Redirect to the dashboard after password change
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'auth/change_firsttime_password.html', {'form': form})



def password_reset_request(request):
    if request.method == "POST":
       
        data = request.POST['email']
        
        user = User.objects.filter(email=data)
        
        if user.exists():
            user = user[0]
            subject = "Password Reset Request"
            email_template_name = "auth/password_reset_email.txt"
            c = {
            "email":user.email, #'domain': '127.0.0.1:8000',
            'domain':'https://buybestfin.in/',
            'site_name': 'Website',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol' : 'https',
         }
            email = render_to_string(email_template_name, c)
            try:
                send_mail( subject,email, 'dvenila@gmail.com' , [user.email], fail_silently=False)
            except BadHeaderError:
                
                return HttpResponse('Invalid header found.')
            return redirect('accounts:password_reset_done')

        messages.info(request,'Invalid Email ID')
    return render(request,'auth/password_reset.html')


def password_reset_done(request):

             return render(request,'auth/password_reset_done.html')
           
        	


def password_reset_confirm(request, *args, **kwargs):
    uidb64 = kwargs.get('uidb64')
    token = kwargs.get('token')
    return render(request,'auth/password_reset_confirm.html',{'token': token, 'uidb64': uidb64})



########################## App Banner ########################

def password_reset_complete(request, *args, **kwargs):
    # import pdb; pdb.set_trace()
    
    if request.method == 'POST':
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
      #  UserModel = get_user_model()

      

        password = request.POST.get("password")
        confirm_password  = request.POST.get("confirm_password")
        uid = urlsafe_base64_decode(uidb64)
        user = User._default_manager.get(pk=uid)

        if password==confirm_password and user is not None and default_token_generator.check_token(user, token):

            try:
                
                user.set_password(password)
                user.save()
                messages.success(request, 'Password Change SuccesFully')

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):

                user = None
        else:
                
                messages.info(request,'password not matching or Password reset link has already been used. Check your email for a new link.')
               
                return render(request,'auth/password_reset_confirm.html',{'token': token, 'uidb64': uidb64})
        

    return render(request,'auth/password_reset_complete.html')



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


# def password_change(request, emp_id):
#     emp_data = get_object_or_404(Employee, emp_user=request.user)
    
#     if request.method == 'POST':
#         form = CustomPasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important to prevent automatic logout
#             messages.success(request, 'Your password was successfully updated!')
#             # return redirect('accounts:index')
#             return redirect('accounts:index', id=request.user)
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)

#     context = {'emp_data': emp_data, 'form': form}
#     # context.update(get_session(request))
#     # request.session.save()

#     return render(request, 'auth/password_change.html', context)

