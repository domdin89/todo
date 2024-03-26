from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy

app_name = 'worksites'
urlpatterns = [
        #get
        path('worksites', views.WorksiteListView.as_view()),
        path('worksites/count', views.worksites_count),
        path('worksites/<int:pk>/', views.WorksiteDetail.as_view()),
        path('worksite-status/<int:id>/', views.get_worksite_status, name='get_worksite_status'),
        path('get-apartment-accesscode', views.get_apartment_accesscode),
        path('get-apartment-accesscode-tecnici', views.get_apartment_accesscode_tecnici),

        path('collabworksites', views.CollaboratorListView.as_view()),

        path('apartment', views.ApartmentListView.as_view()),

        path('worksitesprofile', views.WorksiteProfileListView.as_view()),

        path('worksitesprofile_user', views.WorksiteProfileUserListView.as_view()),
        path('profileWorskite', views.TechnicianNotInWorksiteView.as_view()),

        #post
        path('worksite/new', views.WorksitePostNew),
        path('collabworksite/new', views.new_collabworksite),
        path('category/new', views.new_category),
        path('apartment-new-code', views.apartment_code_generator),
        path('apartment-new-code-tecnici', views.apartment_code_generator_tecnici),
        

        path('profile/update/<int:id>', views.profile_edit),
        path('profile/delete/<int:id>', views.profile_delete),

        path('worksite-status/next', views.update_worksite_status, name='next_worksite_status'),
        path('worksite-status/previous', views.undo_worksite_status, name='undo_worksite_status'),

        #put
        path('worksite-status/date/update', views.update_worksite_status_date, name='date_worksite_status'),
        path('collabworksite/update', views.update_collabworksite),
        path('collabworksites/<int:pk>/', views.CollaboratorUpdateView.as_view()),
        path('collabworksites/reorder', views.edit_order_collabworksite),
        path('worksite/update/<int:worksite_id>', views.update_worksite),
        path('worksite/update/foglio-particella/<int:id>', views.update_foglio_particella),
        path('worksite/update/category/<int:id>', views.update_categories),

        #delete
        path('collabworksite/delete', views.delete_collabworksite),
        path('worksites/delete/<int:id>', views.delete_worksite),
        path('worksites/delete/foglio-particella/<int:id>', views.delete_foglio_particella),
        path('worksites/delete/category/<int:id>', views.delete_category),

        path('collabworksites/delete/<int:id>', views.delete_collaborator),

        
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
