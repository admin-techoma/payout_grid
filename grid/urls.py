from django.urls import path
from . import views

app_name = 'grid'

urlpatterns = [
    path('', views.index, name='index'),
    path('view_grid/', views.view_grid, name='view_grid'),
   
    path('upload_grid/', views.upload_grid, name='upload_grid'),
    path('update_grid/', views.update_grid, name='update_grid'),

    path('ajax/ajax_addrate/', views.ajax_addrate, name='ajax_addrate'),
    path('report_grid/', views.report_grid, name='report_grid'),
    path('ajax/load_product/', views.load_product, name='ajax_load_product'),
    # path('ajax/load_vehical_type/', views.load_vehical_type, name='ajax_load_vehical_type'),
    # path('ajax/load_vehical_subtype/', views.load_vehical_subtype, name='ajax_load_vehical_subtype'),
    path('ajax/load_product_name/', views.load_product_name, name='ajax_load_product_name'),
    path('ajax/load_month/', views.load_month, name='ajax_load_month'),
    path('ajax/load_state/', views.load_state, name='ajax_load_state'),
    path('ajax/load_rto/', views.load_rto, name='ajax_load_rto'),
    
    path('ajax/load_rate_remarks_agent_payout/', views.load_rate_remarks_agent_payout, name='ajax_load_rate_remarks_agent_payout'),

  
]