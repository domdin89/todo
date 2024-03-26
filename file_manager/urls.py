from django.urls import path
from .views import get_directories

urlpatterns = [
    # Altre URL della tua app...
    path('directories/', get_directories, name='get_directories'),
    # Eventuali altre URL...
]
