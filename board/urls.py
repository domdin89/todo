from django.urls import path
from . import views

app_name = 'board'
urlpatterns = [
    path('board/', views.board_lists, name='board'),
    path('boards-lists-api/', views.board_list_api, name='board-lists-api'),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)