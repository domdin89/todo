from django.urls import path
from . import views

urlpatterns = [
    # Altre URL della tua app...
    path('directories/', views.get_directories),
    path('get_file', views.get_file),

    path('directory_new', views.directory_new),
    # Eventuali altre URL...
]
