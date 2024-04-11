from django.urls import path
from . import views

app_name = 'worksites'
urlpatterns = [
        #get
        path('worksites', views.worksites),
        path('apartments', views.apartments),
        path('validate-token', views.apartment_code_validator),

        path('edit_profile', views.edit_profile),
        path('directories-by-apartments', views.get_directories_by_apartments),

        #path('edit-profile', views.edit_profile)
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
