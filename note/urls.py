from django.urls import path

from . import views

urlpatterns = [
    path('label/', views.LabelLC.as_view(), name='label_lc'),
    path('label/<int:pk>', views.LabelRUD.as_view(), name='label_ruc'),
    path('note', views.NoteViewSet.as_view({'post': 'create', 'put': 'update', 'get': 'list'}), name='note'),
    path('note/<int:pk>', views.NoteViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='rd_note'),
    path('archive/', views.IsArchive.as_view(), name='archive'),
    path('trash/', views.IsTrash.as_view(), name='trash'),
    path('archive/<int:id>', views.IsArchive.as_view(), name='archive'),
    path('trash/<int:id>', views.IsTrash.as_view(), name='trash'),
    path('collaborator/<int:id>', views.Collaborator.as_view(), name='collaborator'),


]


