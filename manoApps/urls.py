
from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name='index'),
    path('logged_home/', views.logged_home, name='logged_home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_car/', views.add_car, name='add_car'),
    path('your_car_info/', views.your_car_info, name='your_car_info'),
    path('edit_car/<int:car_id>/<int:carmileage_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/<int:gas_station_id>/', views.delete_car, name='delete_car'),
    path('add_mileage/<int:user_car_id>/', views.add_mileage, name='add_mileage'),
    path('info_service/', views.info_service, name='info_service'),
    path('service_new/', views.service_new, name='service_new'),
    path('service_edit/<int:service_id>/', views.service_edit, name='service_edit'),
    path('service_delete/<int:service_id>/', views.service_delete, name='service_delete'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),



]
