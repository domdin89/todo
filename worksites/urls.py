from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy

app_name = 'worksites'
urlpatterns = [
        path('worksites', views.WorksiteListView.as_view()),
        path('worksites/<int:pk>/', views.WorksiteDetail.as_view()),
        
        path('collabworksites', views.CollaboratorListView.as_view()),
        path('worksitesprofile', views.WorksiteProfileListView.as_view()),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
