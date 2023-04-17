from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='Index'),
    path('logged_home/', views.logged_home, name='logged_home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]
