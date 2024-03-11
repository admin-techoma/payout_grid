from django.urls import path
from . import views

app_name = 'grid'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('user_list/', views.user_list, name='user_list'),
    path('view_grid/', views.view_grid, name='view_grid'),
    
    path('add_employee/', views.add_employee, name='add_employee'),
    path('check-email-exists/', views.check_email_exists, name='check_email_exists'),
    path('check_contact_no_exists/', views.check_contact_no_exists, name='check_contact_no_exists'),
    
    path('upload_grid/', views.upload_grid, name='upload_grid'),
    path('update_grid/', views.update_grid.as_view(), name='update_grid'),
    path('delete_grid/', views.delete_grid, name='delete_grid'),

    path('ajax_update_rate/', views.ajax_update_rate, name='ajax_update_rate'),
    path('report_grid/', views.report_grid, name='report_grid'),
    path('ajax/load_product/', views.load_product, name='ajax_load_product'),
    path('ajax/load_vehical_type/', views.load_vehical_type, name='ajax_load_vehical_type'),
    path('ajax/load_vehical_subtype/', views.load_vehical_subtype, name='ajax_load_vehical_subtype'),
    path('ajax/load_product_name/', views.load_product_name, name='ajax_load_product_name'),
    path('ajax/load_month/', views.load_month, name='ajax_load_month'),
    path('ajax/load_state/', views.load_state, name='ajax_load_state'),
    path('ajax/load_rto/', views.load_rto, name='ajax_load_rto'),
    path('ajax/load_rate_remarks_agent_payout/', views.load_rate_remarks_agent_payout, name='ajax_load_rate_remarks_agent_payout'),

  
]