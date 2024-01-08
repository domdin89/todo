from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CaptchaPasswordResetForm, NewResetForm

app_name = 'accounts'
urlpatterns = [
    #path('login/', views.login_user, name='login'),
    #path('download-list/', views.download_list, name="download-list"),
    #path('download_file/<int:order_id>/<str:filename>/',views.download_file, name="download-file"),

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
