from django.urls import path, include

from . import views

urlpatterns = [
    path('label/', views.LabelLC.as_view(), name='label_lc'),
    path('label/<int:pk>', views.LabelRUD.as_view(), name='label_ruc'),


]
