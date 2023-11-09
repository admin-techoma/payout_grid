from django.urls import path
from . import views

app_name = 'grid'

urlpatterns = [
    path('', views.view_grid, name='view_grid'),


]
