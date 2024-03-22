from django.urls import path
from . import views

app_name = 'worksites'
urlpatterns = [
        #get
        path('worksites', views.worksites),
        path('validate-token', views.apartment_code_validator)
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
