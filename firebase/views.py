from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Firebase, LastVersion
from .serializer import LastVersionSerializer
from datetime import datetime
from rest_framework.permissions import AllowAny, IsAdminUser
import jwt, os, re, requests
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from google.oauth2 import service_account
from google.auth.transport import requests as google_requests
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import json
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes


SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SECRET_KEY = os.environ.get('SECRET_KEY')

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # Explicitly specify no authentication for this view
def token_save(request):
    

    auth_header = request.headers.get('Authorization', '')
    user_id=None,
    if auth_header:
        token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else ''

        decoded_token = AccessToken(token)
        user_id = decoded_token['user_id']
        print(user_id)

    firebase_token = request.data.get('token', None) 
    device_uid = request.data.get('uid', None)
    version = request.data.get('version', '')
    platform = request.data.get('platform', '')

    base_url=os.environ.get('NOTIFICATION_SENDER_URL')
    microservizio_url = f'{base_url}/token_save'
    
    api_key = os.environ.get('NOTIFICATION_SENDER_API_KEY')
    
    headers = {
        'API-Key': f'{api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "firebase_token": firebase_token,
        "platform": platform,
        "device_uid": device_uid,
        "version_installed": version,
        "user": user_id
    }

    response = requests.post(f'{microservizio_url}', headers=headers, json=data)
        
    if response.status_code == 200:
        data = response.json()
        return Response(data)
    else:
        # Se la richiesta non ha avuto successo, restituisci un messaggio di errore
        return Response({'error': 'Impossibile recuperare l\'ultima versione dell\'app dal microservizio'}, status=response.status_code)
    
@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])  # Explicitly specify no authentication for this view
def latest_app(request, platform):
    base_url=os.environ.get('NOTIFICATION_SENDER_URL')
    microservizio_url = f'{base_url}/latest_app?platform={platform}'
    
    api_key = os.environ.get('NOTIFICATION_SENDER_API_KEY')
    
    headers = {
        'API-Key': f'{api_key}'
    }
    
    response = requests.get(f'{microservizio_url}', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return Response(data)
    else:
        # Se la richiesta non ha avuto successo, restituisci un messaggio di errore
        return Response({'error': 'Impossibile recuperare l\'ultima versione dell\'app dal microservizio'}, status=response.status_code)
    

@permission_classes([IsAdminUser]) 
@api_view(['POST'])
def firebase_push(request):

    base_url=os.environ.get('NOTIFICATION_SENDER_URL')
    microservizio_url = f'{base_url}/send_notification'
    
    api_key = os.environ.get('NOTIFICATION_SENDER_API_KEY')
    
    headers = {
        'API-Key': f'{api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "firebase_token": request.data.get('firebase_token', os.environ.get('FIREBASE_APP_NAME')),
        'title': request.data.get('title', os.environ.get('FIREBASE_APP_NAME')),
        'subtitle': request.data.get('subtitle', 'Subtitle'),
        'body': request.data.get('body', 'Corpo della notifica'),
        'silent': request.data.get('silent', None),
        'badge': int(request.data.get('badge', 0)),
        'data1': request.data.get('data1', None),
        'data2': request.data.get('data2', None),
        'path': request.data.get('path', None)

    }

    response = requests.post(f'{microservizio_url}', headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        return Response(data)
    else:
        # Se la richiesta non ha avuto successo, restituisci un messaggio di errore
        return Response({'error': 'Impossibile recuperare l\'ultima versione dell\'app dal microservizio'}, status=response.status_code)
    