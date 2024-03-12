from django.urls import path
from .import views
from django.urls import path
from .views import CustomLoginView

app_name="accounts"

urlpatterns = [
    path('', views.CustomLoginView, name='login'),
    path('change_firsttime_password/', views.change_firsttime_password, name='change_firsttime_password'),
    # forget Password login page
    path('password_reset',views.password_reset_request,name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>/',views.password_reset_confirm,name="password_reset_confirm"),
    path('password_reset_done',views.password_reset_done,name="password_reset_done"),
    path('password_reset_complete/<uidb64>/<token>/',views.password_reset_complete,name="password_reset_complete"),
    path('index/', views.index, name='index'),
        #reset password
    # path('password_change/<str:emp_id>/', views.password_change, name='password_change'),

    # Add other URLs as needed
    path('logout',views.logout,name="logout"),
    
    
]