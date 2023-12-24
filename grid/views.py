from django.shortcuts import render
from grid.models import Product
from decimal import Decimal
from django.db.models import Sum
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .resources import MisResource
from tablib import Dataset
from .models import Grid_data, Grid_file
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import os
from grid.models import Grid_data
from django.core.serializers import serialize
from django.contrib import messages
import tablib
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.views.decorators.cache import cache_control


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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def update_grid(request):
    data = Grid_data.objects.all()

    return render(request, 'update_grid.html',{'data':data})

def ajax_addrate(request):
    addrate = request.GET.get('addrate')
    id = request.GET.get('id')
  
    try:
        grid_data = Grid_data.objects.get(id=id)
        grid_data.rate = addrate
        grid_data.save()

        return JsonResponse({"status": "success", "data": {'rate': addrate, 'id': id}})
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
from django.views.decorators.http import require_GET
@require_GET
def load_product(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list

    # Filter products based on multiple selected companies
    products = Grid_data.objects.filter(company__in=company_ids).order_by('product').values('product').distinct()

    products_list = list(products)
    return JsonResponse({'products': products_list})


#<--------------------- Load vehicle types based on selected company and product----------------------> #
# @require_GET
# def load_vehical_type(request):
#     company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
#     product_id = request.GET.get('product', '')

#     # Filter vehicle types based on multiple selected companies and a product
#     vehical_types = Grid_data.objects.filter(
#         company__in=company_ids,
#         product=product_id
#     ).order_by('vehical_type').values('vehical_type').distinct()

#     vehical_types_list = list(vehical_types)
#     return JsonResponse({'vehical_types': vehical_types_list})
#<--------------------- Load vehicle subtypes based on selected company, product, and vehicle type----------------------> #
# def load_vehical_subtype(request):
#     company = request.GET.get('company')
#     product = request.GET.get('product')
#     vehical_type = request.GET.get('vehical_type')
#     vehical_subtypes = Grid_data.objects.filter(
#         company=company, product=product, vehical_type=vehical_type
#     ).order_by('vehical_subtype').values('vehical_subtype').distinct()
#     vehical_subtypes_list = list(vehical_subtypes)
#     return JsonResponse({'vehical_subtypes': vehical_subtypes_list})

#<---------------------Load product names based on selected company, product, vehicle type, and vehicle subtype----------------------> #
@require_GET
def load_product_name(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')

    # Filter product names based on multiple selected companies and a product
    product_names = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id
    ).order_by('product_name').values('product_name').distinct()

    product_names_list = list(product_names)
    return JsonResponse({'product_names': product_names_list})
#<--------------------- Load months based on selected company, product, vehicle type, vehicle subtype, and product name---------------------> #
@require_GET
def load_month(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')
    product_name_id = request.GET.get('product_name', '')

    # Filter months based on multiple selected companies, a product, and a product name
    months = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
        product_name=product_name_id
    ).order_by('month').values('month').distinct()

    months_list = list(months)
    return JsonResponse({'months': months_list})

#<--------------------Load states based on selected company, product, vehicle type, vehicle subtype, product name, and month---------------------> #

@require_GET
def load_state(request):
    company_ids = request.GET.get('companies', '').split(',')  # Get the comma-separated string and split it into a list
    product_id = request.GET.get('product', '')
    product_name_id = request.GET.get('product_name', '')
    month_id = request.GET.get('month', '')

    # Filter states based on multiple selected companies, a product, a product name, and a month
    states = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
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
    product_name_id = request.GET.get('product_name', '')
    month_id = request.GET.get('month', '')
    state_id = request.GET.get('state', '')

    # Filter RTOs based on multiple selected companies, a product, a product name, a month, and a state
    rtos = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
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
    product_name_id = request.GET.get('product_name', '')
    month_id = request.GET.get('month', '')
    state_id = request.GET.get('state', '')
    rto_id = request.GET.get('rto', '')

    # Query the database based on the filter parameters
    queryset = Grid_data.objects.filter(
        company__in=company_ids,
        product=product_id,
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
            'vehical_type': record.vehical_type,
            'vehical_subtype': record.vehical_subtype,
            # 'rate': record.rate,
            'remarks': record.remarks,
            'rateuser1': record.rateuser1,
            'rateuser2': record.rateuser2,
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