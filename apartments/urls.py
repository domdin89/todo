from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

app_name = 'apartments'
urlpatterns = [
    
    path('clientapartments', views.ClientApartmentsListView.as_view()),

    #get/post
    path('apartments', views.ApartmentListCreateAPIView.as_view(), name='apartments_list_create'),
    path('apartment/new', views.new_apartment),
    path('list-rooms', views.list_rooms),

    #put
    path('apartments/update/<int:id>', views.update_apartment),

    #delete
    path('apartments/delete/<int:id>', views.delete_apartment),

]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
