from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apartments.urls')),
    path('', include('worksites.urls')),
    path('', include('accounts.urls')),
    path('', include('file_manager.urls')),
    path('', include('board.urls')),
    path('', include('firebase.urls')),
    path('api/v1/', include('api.urls')),
    path('.well-known/apple-app-site-association', views.apple_app_site_association, name='apple_app_site_association'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
