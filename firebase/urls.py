
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('token_save', views.token_save),
    path('latest-app-version/<str:platform>', views.latest_app),
    path('send_notification', views.firebase_push),
]
