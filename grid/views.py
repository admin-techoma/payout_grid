from django.shortcuts import render,redirect
from django.http import JsonResponse
from .resources import MisResource
from .models import Grid_data, Grid_file
from django.contrib.auth.decorators import login_required
import os
from grid.models import Grid_data
import tablib
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_control
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
User = get_user_model()


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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=reverse_lazy('accounts:login'))
def update_grid(request):
    data = Grid_data.objects.all()
    paginator = Paginator(data, 25)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # return render(request, "list.html", {"page_obj": page_obj})
    return render(request, 'update_grid.html',{'data':page_obj})

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





class UserRegistrationView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('grid:user_list')  # Default redirect URL

    def form_valid(self, form):
        response = super().form_valid(form)

        # Check if the registered user is a superuser
        if self.object.is_superuser:
            # Update the success_url to redirect superusers to user_list view
            self.success_url = reverse_lazy('grid:user_list')

        return response
    

def user_list(request):

    user= User.objects.all()

    return render(request, 'user_list.html', {'user': user})



