from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('login-as/', views.login_as, name='login-as'),

    path('reset-password/', views.reset_password, name='reset_password'),

    path('password/test/', views.recover_password, name='password_reset_request'),
    path('password/reset/', views.password_reset_request, name='password_reset_request'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-confirm-done/', views.password_reset_new, name='password_reset_confirm_done'),
    path('reset-password-done/', views.password_reset_done, name='password_reset_done')

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)