from django.urls import path
from . import views

app_name = 'grid'

urlpatterns = [
    path('', views.view_grid, name='view_grid'),
    path('upload_grid/', views.upload_grid, name='upload_grid'),
    path('ajax/load_vehical_type/', views.load_vehical_type, name='ajax_load_vehical_type'),
  
]


