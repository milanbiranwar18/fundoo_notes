from django.urls import path, include

from . import views

urlpatterns = [
    path('user_registration/', views.Registration.as_view({'post': 'create'}), name='registration'),
    path('user_login/', views.Login.as_view({'post': 'create'}), name='login'),
    path('user_logout/', views.LogoutAPI.as_view(), name='user_logout'),

    path('user_reg/', views.user_registration, name = 'user_registration'),
    path('login/', views.user_login, name ='user_login'),
    path('logout/', views.user_logout, name ='user_logout'),
    path('home_page/', views.home_page, name='home_page'),





]
