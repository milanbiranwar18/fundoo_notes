from django.urls import path, include

from . import views

urlpatterns = [
    path('user_registration/', views.Registration.as_view({'post': 'create'}), name='registration'),
    path('user_login/', views.Login.as_view({'post': 'create'}), name='login'),



]
