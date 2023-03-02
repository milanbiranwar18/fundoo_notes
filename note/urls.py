from django.urls import path

from . import views

urlpatterns = [
    path('label/', views.LabelLC.as_view(), name='label_lc'),
    path('label/<int:pk>', views.LabelRUD.as_view(), name='label_ruc'),
    path('note', views.NoteViewSet.as_view({'post': 'create', 'get': 'list'}), name='note'),
    path('note/<int:pk>', views.NoteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='note'),



]
