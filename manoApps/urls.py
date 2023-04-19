from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='Index'),
    path('logged_home/', views.logged_home, name='logged_home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_car/', views.add_car, name='add_car'),
    path('your_car_info/', views.your_car_info, name='your_car_info'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),

]
