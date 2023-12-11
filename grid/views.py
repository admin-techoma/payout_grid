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




def view_grid(request):
    products = Grid_data.objects.values('product').distinct()
    context = {
        'products': products
    }
    return render(request, 'view_grid.html', context)

from django.http import JsonResponse

from django.http import JsonResponse
from django.core.serializers import serialize

def load_vehical_type(request):
    product = request.GET.get('product')
    vehical_types = Grid_data.objects.filter(product=product).order_by('vehical_type').values('vehical_type').distinct()
    
    # Convert the QuerySet to a list of dictionaries
    vehical_types_list = list(vehical_types)
    
    # You can use Django's built-in serializers to serialize the data
    # serialized_data = serialize('json', vehical_types, fields=('vehical_type',))
    
    return JsonResponse({'vehical_types': vehical_types_list})




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
