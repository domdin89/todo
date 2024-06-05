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
        path('worksite-detail', views.worksite_detail),
        path('apartments', views.apartments),
        path('apartments-app', views.ApartmentListViewApp.as_view()),
        path('boards', views.boards),
        path('validate-token', views.apartment_code_validator),

        path('edit_profile', views.edit_profile),
        path('edit_profile-partial', views.edit_profile_partial),
        path('directories', views.get_directories),
        path('directories-by-apartments', views.get_directories_by_apartments),
        path('get-privacy', views.get_privacy),
        path('get-profile', views.get_profile),
        
        path('worksite/update/<int:worksite_id>', views.update_worksite),
        path('directory_new', views.directory_new),
        path('file_new', views.file_new),

        path('password/reset', views.password_reset_request, name='password_reset_request'),
        path('password/reset/confirm', views.password_reset_confirm, name='password_reset_confirm'),
        ]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
