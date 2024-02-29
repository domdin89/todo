from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy

app_name = 'worksites'
urlpatterns = [
        #get
        #path('prova', views.prova),
        path('worksites', views.WorksiteListView.as_view()),
        path('worksites/<int:pk>', views.WorksiteDetail.as_view()),

        path('collabworksites', views.CollaboratorListView.as_view()),

        path('worksitesprofile', views.WorksiteProfileListView.as_view()),

        path('worksitesprofile_user', views.WorksiteProfileUserListView.as_view()),
        path('profileWorskite', views.TechnicianNotInWorksiteView.as_view()),

        #post
        path('worksite/new', views.WorksitePostNew),
        path('collabworksite/new', views.new_collabworksite),
        path('category/new', views.new_category),

        #put
        path('collabworksite/update', views.update_collabworksite),
        path('collabworksites/<int:pk>/', views.CollaboratorUpdateView.as_view()),
        path('worksites/update/<int:worksite_id>', views.update_worksite),
        path('worksites/update/foglio-particella/<int:id>', views.update_foglio_particella),
        path('worksites/update/category/<int:id>', views.update_categories),

        #delete
        path('worksites/delete/<int:id>', views.delete_worksite),
        path('worksites/delete/foglio-particella/<int:id>', views.delete_foglio_particella),
        path('worksites/delete/category/<int:id>', views.delete_category),

        path('collabworksites/delete/<int:id>', views.delete_collaborator),

        
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
