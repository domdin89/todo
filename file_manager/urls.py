from django.urls import path
from .views import get_directories, get_file

urlpatterns = [
    # Altre URL della tua app...
    path('directories/', get_directories, name='get_directories'),
    path('get_file', get_file, name='get_file'),
    # Eventuali altre URL...
]
