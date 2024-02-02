from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('boards', views.BoardsListView.as_view(), name='boards-list'),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)