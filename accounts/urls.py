from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('login', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('profiles1', views.ProfileListCreateAPIView2.as_view()),

    path('profiles2', views.ProfileListAPIView.as_view()),
    path('worksites2', views.WorksiteListAPIView.as_view()),
    path('collabworksites2', views.CollabWorksiteListAPIView.as_view()),

    path('profiles', views.get_profiles),
    path('profile-new', views.profile_create),
]
