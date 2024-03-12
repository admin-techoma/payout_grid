from django.shortcuts import render,redirect
from django.http import JsonResponse
from .resources import MisResource
from .models import Employee, Grid_data, Grid_file
from django.contrib.auth.decorators import login_required
import os
from grid.models import Grid_data
import tablib
from django.contrib import messages
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_control
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.generic import ListView
from django.core.mail import  send_mail
from core import settings
from django.core.paginator import Paginator

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def index(request):

    return render(request,'index.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def upload_grid(request):
    context = {}
    result = None  # Default value for result

    data = Grid_file.objects.all()

    if request.method == 'POST':
        mis_resource = MisResource()
        dataset = tablib.Dataset()
        new_grid = request.FILES['myfile']

        details = Grid_file.objects.create(user=request.user, uploaded_file=new_grid)
        dataset.load(details.uploaded_file.read(), format='xlsx')

        result = mis_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            mis_resource.import_data(dataset, dry_run=False)

        data = Grid_file.objects.all()
     
    context = {'data': data, 'result': result}
    return render(request, 'uploadgrid.html', context)


def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('field1', 'field2'):
            return 'My custom error message'
        else:
            return super(Grid_data, self).unique_error_message(model_class, unique_check)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def view_grid(request):
    companys= Grid_data.objects.values('company').distinct()
    context = {
        'companys':companys
    }
    return render(request, 'view_grid.html', context)


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url=reverse_lazy('accounts:login'))
# def update_grid(request):
#     data = Grid_data.objects.all()
#     # import pdb ; pdb.set_trace()
#     paginator = Paginator(data, len(data))  # Show 25 contacts per page.
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     # return render(request, "list.html", {"page_obj": page_obj})
#     return render(request, 'update_grid.html',{'data':page_obj})

class update_grid(ListView):
    model = Grid_data
    template_name = 'update_grid.html'
    context_object_name = 'data'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        qs = Grid_data.objects.all()
        # if query is not None:
        #     qs=qs.filter( Q(buyer__name__icontains=query) | Q(dn_no__icontains=query) | Q(sales_order__so_no__icontains=query) )
        return qs

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def delete_grid(request):
    if request.method == 'POST':
        Grid_data.objects.all().delete()
        return redirect('grid:delete_grid')  # Redirect to a success page or any desired URL
    
    return render(request, 'delete_griddata.html')



def ajax_update_rate(request):
    if request.method == 'GET':
        rate_od = request.GET.get('rate_od')
        rate_tp= request.GET.get('rate_tp')
        company= request.GET.get('company')
        product= request.GET.get('product')
        vehical_type= request.GET.get('vehical_type')
        vehical_subtype= request.GET.get('vehical_subtype')
        product_name= request.GET.get('product_name')
        month= request.GET.get('month')
        state= request.GET.get('state')
        rto= request.GET.get('rto')
        remarks= request.GET.get('remarks')
        rate_net= request.GET.get('rate_net')
        rateuser1_od= request.GET.get('rateuser1_od')
        rateuser1_tp= request.GET.get('rateuser1_tp')
        rateuser1_net= request.GET.get('rateuser1_net')
        rateuser2_od= request.GET.get('rateuser2_od')
        rateuser2_tp= request.GET.get('rateuser2_tp')
        rateuser2_net= request.GET.get('rateuser2_net')
        rateuser3_od= request.GET.get('rateuser3_od')
        rateuser3_tp= request.GET.get('rateuser3_tp')
        rateuser3_net= request.GET.get('rateuser3_net')
        pk = request.GET.get('pk')

        try:
            grid_data = Grid_data.objects.get(pk=pk)
            grid_data.rate_od = rate_od  # Update the specific field (change as needed)
            grid_data.rate_tp = rate_tp
            grid_data.rate_net = rate_net
            grid_data.company = company
            grid_data.product = product
            grid_data.product_name = product_name
            grid_data.month = month
            grid_data.state = state
            grid_data.rto = rto
            grid_data.remarks = remarks
            grid_data.vehical_type = vehical_type
            grid_data.vehical_subtype = vehical_subtype
            grid_data.rateuser1_od = rateuser1_od
            grid_data.rateuser1_tp = rateuser1_tp
            grid_data.rateuser1_net = rateuser1_net
            grid_data.rateuser2_od = rateuser2_od
            grid_data.rateuser2_tp = rateuser2_tp
            grid_data.rateuser2_net = rateuser2_net
            grid_data.rateuser3_od = rateuser3_od
            grid_data.rateuser3_tp = rateuser3_tp
            grid_data.rateuser3_net = rateuser3_net
            grid_data.save()

            return JsonResponse({"status": "success", "data": {'rate_od': rate_od,'rate_tp': rate_tp,'rate_net':rate_net,'company': company,'product': product,'vehical_type':vehical_type,'vehical_subtype':vehical_subtype,'product_name':product_name,'month':month,'state':state,'rto':rto,'remarks':remarks,'rate_userone_od':rateuser1_od,'rate_userone_tp':rateuser1_tp,'rate_userone_net':rateuser1_net,'rate_usertwo_od':rateuser2_od,'rate_usertwo_tp':rateuser2_tp,'rate_usertwo_net':rateuser2_net,'rate_userthree_od':rateuser3_od,'rate_userthree_tp':rateuser3_tp,'rate_userthree_net':rateuser3_net,'pk': pk}})
        except Grid_data.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Record not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def report_grid(request):

    return render(request, 'report_grid.html')


#<--------------------- AJAX Load----------------------> #

#<--------------------- Load Product based on company----------------------> #

@require_GET
def load_product(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list

    # Filter products based on multiple selected companies
    products = Grid_data.objects.filter(company__in=company_ids).order_by('product').values('product').distinct()

    products_list = list(products)
    return JsonResponse({'products': products_list})


#<--------------------- Load vehicle types based on selected company and product----------------------> #
@require_GET
def load_vehical_type(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')

    # Filter vehicle types based on multiple selected companies and a product
    vehical_types = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id
    ).order_by('vehical_type').values('vehical_type').distinct()

    vehical_types_list = list(vehical_types)
    return JsonResponse({'vehical_types': vehical_types_list})
#<--------------------- Load vehicle subtypes based on selected company, product, and vehicle type----------------------> #
def load_vehical_subtype(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')
    vehical_type = request.GET.get('vehical_type','')
    vehical_subtypes = Grid_data.objects.filter(
        company__in=company_ids, product=product_id, vehical_type=vehical_type
    ).order_by('vehical_subtype').values('vehical_subtype').distinct()
    vehical_subtypes_list = list(vehical_subtypes)
    return JsonResponse({'vehical_subtypes': vehical_subtypes_list})

#<---------------------Load product names based on selected company, product, vehicle type, and vehicle subtype----------------------> #
@require_GET
def load_product_name(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')
    vehical_type = request.GET.get('vehical_type','')
    vehical_subtype = request.GET.get('vehical_subtype','')

    # Filter product names based on multiple selected companies and a product
    product_names = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
        vehical_type=vehical_type,
        vehical_subtype=vehical_subtype
    ).order_by('product_name').values('product_name').distinct()

    product_names_list = list(product_names)
    return JsonResponse({'product_names': product_names_list})
#<--------------------- Load months based on selected company, product, vehicle type, vehicle subtype, and product name---------------------> #
@require_GET
def load_month(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')
    vehical_type = request.GET.get('vehical_type','')
    vehical_subtype = request.GET.get('vehical_subtype','')
    product_name_id = request.GET.get('product_name', '')

    # Filter months based on multiple selected companies, a product, and a product name
    months = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
        vehical_type=vehical_type,
        vehical_subtype=vehical_subtype,
        product_name=product_name_id
    ).order_by('month').values('month').distinct()

    months_list = list(months)
    return JsonResponse({'months': months_list})

#<--------------------Load states based on selected company, product, vehicle type, vehicle subtype, product name, and month---------------------> #

@require_GET
def load_state(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')
    vehical_type = request.GET.get('vehical_type','')
    vehical_subtype = request.GET.get('vehical_subtype','')
    product_name_id = request.GET.get('product_name', '')
    month_id = request.GET.get('month', '')

    # Filter states based on multiple selected companies, a product, a product name, and a month
    states = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
        vehical_type=vehical_type,
        vehical_subtype=vehical_subtype,
        product_name=product_name_id,
        month=month_id
    ).order_by('state').values('state').distinct()

    states_list = list(states)
    return JsonResponse({'states': states_list})
#<--------------------Load RTOs based on selected company, product, vehicle type, vehicle subtype, product name, month, and state---------------------> #

@require_GET
def load_rto(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')
    vehical_type = request.GET.get('vehical_type','')
    vehical_subtype = request.GET.get('vehical_subtype','')
    product_name_id = request.GET.get('product_name', '')
    month_id = request.GET.get('month', '')
    state_id = request.GET.get('state', '')

    # Filter RTOs based on multiple selected companies, a product, a product name, a month, and a state
    rtos = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
        vehical_type=vehical_type,
        vehical_subtype=vehical_subtype,
        product_name=product_name_id,
        month=month_id,
        state=state_id
    ).order_by('rto').values('rto').distinct()

    rtos_list = list(rtos)
    return JsonResponse({'rtos': rtos_list})

#<-------------------Load Rate, Remarks, and Agent Rate based on selected company, product, vehicle type, vehicle subtype, product name, month, state, and rto---------------------> #



@require_GET
def load_rate_remarks_agent_payout(request):
    # Extract filter parameters from the GET request
    company_ids = request.GET.get('company', '').split(',')
    product_id = request.GET.get('product', '')
    vehical_type = request.GET.get('vehical_type','')
    vehical_subtype = request.GET.get('vehical_subtype','')
    product_name_id = request.GET.get('product_name', '')
    month_id = request.GET.get('month', '')
    state_id = request.GET.get('state', '')
    rto_id = request.GET.get('rto', '')

    # Query the database based on the filter parameters
    queryset = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
        vehical_type =vehical_type,
        vehical_subtype=vehical_subtype,
        product_name=product_name_id,
        month=month_id,
        state=state_id,
        rto=rto_id
    )

    # Prepare the data to be sent as JSON
    results = []
    for record in queryset:
        result_dict = {
            'company': record.company,
            # 'vehical_type': record.vehical_type,
            # 'vehical_subtype': record.vehical_subtype,
            # 'rate': record.rate,
            'remarks': record.remarks,
            'rateuser1_od': record.rateuser1_od,
            'rateuser1_tp': record.rateuser1_tp,
            'rateuser1_net': record.rateuser1_net,
            'rateuser2_od': record.rateuser2_od,
            'rateuser2_tp': record.rateuser2_tp,
            'rateuser2_net': record.rateuser2_net,
            'rateuser3_od': record.rateuser3_od,
            'rateuser3_tp': record.rateuser3_tp,
            'rateuser3_net': record.rateuser3_net,
        }
        results.append(result_dict)

    return JsonResponse({'results': results})



def dash(request):
    username = request.session.get('user_username', '')
    print(f'HR Dashboard - Logged in as: {username}')
    # Your HR dashboard logic here
    return render(request, 'view_grid.html', {'username':username})
    # if request.user.is_authenticated:
    #     return redirect('hr:dash')
    # employee = Employee.objects.get(emp_user=request.user) 
   
 
    # return render(request,'hr/hrdashboard.html',{ 'emp':employee.emp_user})
    # return render(request,'hr/hrdashboard.html')




    

def user_list(request):

    user= User.objects.all()

    return render(request, 'user_list.html', {'user': user})


def generate_next_emp_id():
    last_employee = Employee.objects.last()
    if last_employee:
        last_emp_id = last_employee.emp_id
        emp_number = int(last_emp_id[5:]) + 1
        return f'NIBPL{str(emp_number).zfill(3)}'
    else:
        return 'NIBPL001'

def check_email_exists(request):
    email = request.GET.get('email', None)
    exists = Employee.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

def check_contact_no_exists(request):
    contact_no = request.GET.get('contact_no', None)
    exists = Employee.objects.filter(contact_no=contact_no).exists()
    return JsonResponse({'exists': exists})


from django.contrib.auth.models import Group

from django.contrib.auth.models import Group

def add_employee(request):
    emp = Employee.objects.all()
    emp_id = generate_next_emp_id()
    groups = Group.objects.all()  # Fetch all available groups
    # Initialize email, contact_no, name, and status outside the if statement
    email = None
    contact_no = None
    name = None
    status = None

    if request.method == 'POST':
        emp_id = request.POST.get("emp_id")
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact_no = request.POST.get("contact_no")
        status = "Active"
        group_id = request.POST.get("group")  # Added to retrieve selected group ID

        # Check if email or contact number already exists
        if Employee.objects.filter(email=email).exists():
            messages.error(request, 'Email Id Already Exists.')
        elif Employee.objects.filter(contact_no=contact_no).exists():
            messages.error(request, 'Contact Number Already Exists.')
        else:
            # If neither email nor contact number exists, create the employee
            employee_instance = Employee.objects.create(emp_id=emp_id, name=name, email=email, contact_no=contact_no, status=status)

            # Create or get the user associated with the employee
            user, created = User.objects.get_or_create(username=email, email=email, first_name=name)

            # Set the password for the user if it's a new user
            if created:
                password = User.objects.make_random_password(length=8)
                user.set_password(password)
                user.save()

            # Associate the user with the employee
            employee_instance.emp_user = user

            # Assign the selected group to the employee
            if group_id:
                group = Group.objects.get(id=group_id)
                employee_instance.group = group

                # Add the user to the selected group
                user.groups.set([group])

            employee_instance.save()

            # Send email to the employee with username and password
            subject = 'Employee Portal Access Credentials Verification'
            message = f"""Dear {name},

            We trust this email finds you well. We would like to inform you that your details have been successfully verified, and we are pleased to provide you with the login credentials for accessing the Payout Grid Portal.

            Here are your login details:
            URL     : https://buybestfin.in/
            Username: {employee_instance.email}
            Password: {password}

            please chnage givan password on first time login.    
            Please ensure the confidentiality of your login credentials and do not share them with anyone. If you have any concerns or questions regarding the login process, feel free to reach out to our HR department.

            Best Regards,
            Techoma Technologies Pvt. Ltd.
            Human Resources Department."""
            
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [employee_instance.email]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, 'Employee Created Successfully!')
            return redirect('grid:user_list')



    context = {
        'emp_id': emp_id,
        'emp': emp,
        'groups': groups,  # Pass the groups to the template
    }

    return render(request, 'add_employee.html', context)


