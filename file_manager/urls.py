from django.urls import path
from . import views

urlpatterns = [
    # Altre URL della tua app...
    path('directories/', views.get_directories),
    path('get_file', views.get_file),

    path('directory_new', views.directory_new),
    path('permission-dir', views.permission_directory),
    path('permission-reset', views.reset_permission),
    path('directory-delete', views.delete_directory),

    path('permission-file', views.permission_file),
    path('permission-reset-file', views.reset_file_permission),

    path('file-delete', views.delete_file),

    path('file_new', views.file_new),
    # Eventuali altre URL...
]
