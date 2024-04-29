from django.urls import path
from . import views

app_name = 'worksites'
urlpatterns = [
        path('register', views.register),
        path('register-confirm', views.confirm_account),
        path('delete-account', views.delete_account),
        path('confirm-account', views.confirm_account),
        #get
        path('worksites', views.worksites),
        path('apartments', views.apartments),
        path('boards', views.boards),
        path('validate-token', views.apartment_code_validator),

        path('edit_profile', views.edit_profile),
        path('edit_profile-partial', views.edit_profile_partial),
        path('directories', views.get_directories),
        path('directories-by-apartments', views.get_directories_by_apartments),
        path('get-privacy', views.get_privacy),
        path('get-profile', views.get_profile),
        #path('edit-profile', views.edit_profile)
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
