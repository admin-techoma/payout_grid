from django.urls import path
from .import views
from django.urls import path
from .views import CustomLoginView

app_name="accounts"

urlpatterns = [
    path('', views.CustomLoginView, name='login'),
    path('index/', views.index, name='index'),
    # Add other URLs as needed
    path('logout',views.logout,name="logout"),
]