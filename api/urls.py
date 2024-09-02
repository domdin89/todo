from django.urls import path
from . import views

app_name = 'worksites'
urlpatterns = [
        #GET
        path('tasks', views.get_tasks),
        path('task-history', views.history_tasks),

        #POST
        path('task', views.new_task),

        #PUT
        path('task', views.update_tasks),

        #DELETE
        path('task-delete', views.delete_tasks)
        ]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
