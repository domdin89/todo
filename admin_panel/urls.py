from django.urls import path
from . import views

app_name = 'admin_panel'
urlpatterns = [
    path('', views.admin, name='admin'),
    path('worksites/', views.worksites, name='worksites'),

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)