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

@login_required(login_url=reverse_lazy('login'))
def index(request):

    return render(request,'index.html')


def view_grid(request):
    companys= Grid_data.objects.values('company').distinct()
    context = {
        'companys':companys
    }
    return render(request, 'view_grid.html', context)

def load_product(request):
    # import pdb ; pdb.set_trace()
    company = request.GET.get('company')  # Correct parameter name
    products = Grid_data.objects.filter(company=company).order_by('product').values('product').distinct()
    products_list = list(products)
    return JsonResponse({'products': products_list})

def load_vehical_type(request):
    company = request.GET.get('company')
    product = request.GET.get('product')
    vehical_types = Grid_data.objects.filter(company=company, product=product).order_by('vehical_type').values('vehical_type').distinct()
    vehical_types_list = list(vehical_types)
    return JsonResponse({'vehical_types': vehical_types_list})



def load_vehical_subtype(request):
    company = request.GET.get('company')
    product = request.GET.get('product')
    vehical_type = request.GET.get('vehical_type')
    vehical_subtypes = Grid_data.objects.filter(
        company=company, product=product, vehical_type=vehical_type
    ).order_by('vehical_subtype').values('vehical_subtype').distinct()
    vehical_subtypes_list = list(vehical_subtypes)
    return JsonResponse({'vehical_subtypes': vehical_subtypes_list})

def load_product_name(request):
    company = request.GET.get('company')
    product = request.GET.get('product')
    vehical_type = request.GET.get('vehical_type')
    vehical_subtype = request.GET.get('vehical_subtype')
    product_names = Grid_data.objects.filter(
        company=company, product=product, vehical_type=vehical_type, vehical_subtype=vehical_subtype
    ).order_by('product_name').values('product_name').distinct()
    product_names_list = list(product_names)
    return JsonResponse({'product_names': product_names_list})

def load_month(request):
    company = request.GET.get('company')
    product = request.GET.get('product')
    vehical_type = request.GET.get('vehical_type')
    vehical_subtype = request.GET.get('vehical_subtype')
    product_name = request.GET.get('product_name')
    months = Grid_data.objects.filter(
        company=company, product=product, vehical_type=vehical_type, vehical_subtype=vehical_subtype, product_name=product_name
    ).order_by('month').values('month').distinct()
    months_list = list(months)
    return JsonResponse({'months': months_list})

def load_state(request):
    company = request.GET.get('company')
    product = request.GET.get('product')
    vehical_type = request.GET.get('vehical_type')
    vehical_subtype = request.GET.get('vehical_subtype')
    product_name = request.GET.get('product_name')
    month = request.GET.get('month')
    states = Grid_data.objects.filter(
        company=company, product=product, vehical_type=vehical_type, vehical_subtype=vehical_subtype, product_name=product_name, month=month
    ).order_by('state').values('state').distinct()
    states_list = list(states)
    return JsonResponse({'states': states_list})

def load_rto(request):
    company = request.GET.get('company')
    product = request.GET.get('product')
    vehical_type = request.GET.get('vehical_type')
    vehical_subtype = request.GET.get('vehical_subtype')
    product_name = request.GET.get('product_name')
    month = request.GET.get('month')
    state = request.GET.get('state')

    # Your logic to filter and get RTOs based on the provided parameters
    # Example:
    rtos = Grid_data.objects.filter(
        company=company,
        product=product,
        vehical_type=vehical_type,
        vehical_subtype=vehical_subtype,
        product_name=product_name,
        month=month,
        state=state
    ).order_by('rto').values('rto').distinct()

    rtos_list = list(rtos)
    return JsonResponse({'rtos': rtos_list})

def load_rate_remarks_agent_payout(request):
    company = request.GET.get('company')
    product = request.GET.get('product')
    vehical_type = request.GET.get('vehical_type')
    vehical_subtype = request.GET.get('vehical_subtype')
    product_name = request.GET.get('product_name')
    month = request.GET.get('month')
    state = request.GET.get('state')
    rto = request.GET.get('rto')

    # Your logic to filter and get Rate, Remarks, and Agent Rate based on the provided parameters
    # Example:
    data = Grid_data.objects.filter(
        company=company,
        product=product,
        vehical_type=vehical_type,
        vehical_subtype=vehical_subtype,
        product_name=product_name,
        month=month,
        state=state,
        rto=rto
    ).values('rate', 'remarks', 'agent_payout').first()

    return JsonResponse({
        'rate': data['rate'] if data else '',
        'remarks': data['remarks'] if data else '',
        'agent_payout': data['agent_payout'] if data else '',
    })



@login_required(login_url=reverse_lazy('login'))
def upload_grid(request):
    
    context = {}  # Define context here to ensure it is always defined
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



# from django.http import JsonResponse

# def get_rate_and_payout(request):
#     if request.method == 'GET':
#         product = request.GET.get('product', '')
#         vehical_type = request.GET.get('vehical_type', '')
#         vehical_subtype = request.GET.get('vehical_subtype', '')
        
        
#         grid_data = Grid_data.objects.get(
#             product=product,
#             vehical_type=vehical_type,
#             vehical_subtype=vehical_subtype,
#         )
#         data = {
#             'rate': grid_data.rate,
#             'remarks': grid_data.remarks,
#             'agent_payout': grid_data.agent_payout,
#         }
#         return redirect('grid:upload_grid',data)
#     #        return JsonResponse(data)
#     #     except Grid_data.DoesNotExist:
#     #         return JsonResponse({'error': 'Data not found'}, status=404)

# #     # return JsonResponse({'error': 'Invalid request'}, status=400)
# def insurance_rate_remarks(request):
#     if request.method == 'POST':
#         selected_company = request.POST.get('company')
#         selected_product = request.POST.get('product')

#         # Fetch data based on user selection
#         matching_data = Grid_data.objects.filter(company=selected_company, product=selected_product).first()

#         if matching_data:
#             rate = matching_data.rate
#             remarks = matching_data.remarks
#         else:
#             rate = None
#             remarks = None

#         return render(request, 'your_template.html', {'rate': rate, 'remarks': remarks})
#     else:
#         # Handle the initial GET request, maybe render a form with dropdowns for company and product
#         return render(request, 'your_template.html', {})