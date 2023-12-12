from django.shortcuts import render
from grid.models import Product
from decimal import Decimal
from django.db.models import Sum
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import JsonResponse
from .resources import MisResource
from tablib import Dataset
from .models import Grid_data,Grid_file, grid_doc_path
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import os
from grid.models import Grid_data
from django.core.serializers import serialize



def view_grid(request):
    products = Grid_data.objects.values('product').distinct()
    context = {
        'products': products
    }
    return render(request, 'view_grid.html', context)



def load_vehical_type(request):
    product = request.GET.get('product')
    vehical_types = Grid_data.objects.filter(product=product).order_by('vehical_type').values('vehical_type').distinct()
    vehical_types_list = list(vehical_types)
    return JsonResponse({'vehical_types': vehical_types_list})

def load_vehical_subtype(request):
    vehical_type = request.GET.get('vehical_type')
    vehical_subtypes = Grid_data.objects.filter(vehical_type=vehical_type).order_by('vehical_subtype').values('vehical_subtype').distinct()
    vehical_subtypes_list = list(vehical_subtypes)
    return JsonResponse({'vehical_subtypes': vehical_subtypes_list})

def load_product_name(request):
    vehical_subtype = request.GET.get('vehical_subtype')
    product_names = Grid_data.objects.filter(vehical_subtype=vehical_subtype).order_by('product_name').values('product_name').distinct()
    product_names_list = list(product_names)
    print("product_names_list************",product_names_list)
    return JsonResponse({'product_names': product_names_list})

def load_company(request):
    # import pdb ; pdb.set_trace()
    product_name = request.GET.get('company')  # Correct parameter name
    companys = Grid_data.objects.filter(product_name=product_name).order_by('company').values('company').distinct()
    companys_list = list(companys)
    
    return JsonResponse({'companys': companys_list})



def load_month(request):
    # import pdb ; pdb.set_trace()
    company = request.GET.get('month')  # Correct parameter name
    months = Grid_data.objects.filter(company=company).order_by('month').values('month').distinct()
    months_list = list(months)
    
    return JsonResponse({'months': months_list})

def load_state(request):
    # import pdb ; pdb.set_trace()
    month = request.GET.get('state')  # Correct parameter name
    states = Grid_data.objects.filter(month=month).order_by('state').values('state').distinct()
    states_list = list(states)
    
    return JsonResponse({'states': states_list})

def load_rto(request):
    # import pdb ; pdb.set_trace()
    state = request.GET.get('rto')  # Correct parameter name
    rtos = Grid_data.objects.filter(state=state).order_by('rto').values('rto').distinct()
    rtos_list = list(rtos)
    
    return JsonResponse({'rtos': rtos_list})


def reco_doc_path(instance,filename):
    return 'reco_files/{0}'.format(instance.created_on,filename)

def upload_grid(request):

    if request.method == 'POST':
        mis_resource = MisResource()
        dataset = Dataset()
        new_mis = request.FILES['myfile']

        dataset.load(new_mis.read(),format='xlsx')

        result = mis_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            mis_resource.import_data(dataset, dry_run=False)
        
        context = {'result':result}
    return render(request,'uploadgrid.html',context)

def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('field1', 'field2'):
            return 'My custom error message'
        else:
            return super(Grid_data, self).unique_error_message(model_class, unique_check)
