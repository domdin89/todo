from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Firebase, LastVersion
from .serializer import LastVersionSerializer
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
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


SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
SECRET_KEY = os.environ.get('SECRET_KEY')

@permission_classes([AllowAny])
@api_view(['POST'])
def token_save(request):
    try:
        token = request.data.get('token', None)  # Default value is None
        uid = request.data.get('uid', None)
        version = request.data.get('version', '')
        platform = request.data.get('platform', '')

        userId = None

        # Decode JWT token if present
        auth_header = request.headers.get('Authorization', '')
        jwt_token = None

        if auth_header.startswith('Bearer '):
            jwt_token = auth_header.split(' ')[1]

        if jwt_token:
            try:
                decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
                profile_id = decoded_token.get('cliente')
                userId = profile_id
            except ExpiredSignatureError:
                return Response({'message': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                print('JWT decode exception: ', e)

        # Handle case where userId is None
        if userId is None:
            userId = ""

        try:
            if token:
                get_uid = Firebase.objects.get(token=token)
                get_uid.consent = True
                get_uid.uid = uid if uid else get_uid.uid
            else:
                get_uid = Firebase.objects.get(uid=uid)
                get_uid.consent = False

            get_uid.version = version if version else get_uid.version
            get_uid.platform = platform if platform else get_uid.platform
            get_uid.last_access = timezone.now() 
            get_uid.count += 1  
            get_uid.userId = userId

            get_uid.save()

        except Firebase.DoesNotExist:
            create_params = {
                'userId': userId,
                'consent': True if token else False,
                'version': version,
                'platform': platform,
                'last_access': timezone.now(),
                'additional_params': "",
                'count': 1,
            }
            
            if token:
                create_params['token'] = token
            if uid:
                create_params['uid'] = uid

            Firebase.objects.create(**create_params)

    except Exception as e:
        print(f"Token_error occurred: {e}")
        return Response({'message': f'An error occurred: {e}'}, status=status.HTTP_200_OK)

    return Response({'message': 'Token salvato correttamente'}, status=status.HTTP_200_OK)

def get_clienti_based_on_type(userId, notification_type):
    print(notification_type)
    firebases = Firebase.objects.filter(userId=userId)
    
    matching_firebases = []

    for firebase in firebases:
        permissions_data = firebase.permissions
        print(permissions_data)
    
        if notification_type == 'Default':
            matching_firebases.append(firebase)
        elif notification_type == 'carichi' and permissions_data['carichi']:
            matching_firebases.append(firebase)
        elif notification_type == 'rifornimenti' and permissions_data['rifornimenti']:
            matching_firebases.append(firebase)
        elif 'types' in permissions_data:
            print('entro qui')
            type_numbers = {item['id'] for item in permissions_data['types']}
            print('type_numbers',type_numbers)
            print('notification_type.isdigit()',notification_type.isdigit())
            if notification_type.isdigit() and int(notification_type) in type_numbers:
                matching_firebases.append(firebase)

    return matching_firebases

def send_firebase_notification(request, userId, title, subtitle, body, badge, silent=None, data1=None, data2=None, path=None, type='Default'):

    if silent:
        title = ''
        subtitle = ''
        body = ''

    Authorization = 'Bearer '+ _get_access_token()
    Host = 'fcm.googleapis.com'
    url = f"https://fcm.googleapis.com/v1/projects/{os.environ.get('FIREBASE_PROJECT_ID')}/messages:send"
    
    clienti = get_clienti_based_on_type(userId, type)

    response = None

    if not clienti:
        print(f"No tokens found for userId: {userId}")
        # Optionally, return some default response or raise an exception
        return

    for token in clienti:
        token = token.token

        headers = {
            'Authorization': Authorization,
            'Host': Host,
            'Content-Type': 'application/json',
        }

        data = {
            "message":{
                "android": {
                    "notification": {
                        "image": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
                    }
                },
                "apns": {
                    "headers": {
                        "apns-priority": "5"
                    },
                    "payload": {
                        "aps": {
                            "badge" : badge,
                            "sound" : {
                                "critical": 1,
                                "name":"bingbong.aiff",
                                "volume": 1
                            },
                            "alert" : {
                                "title" : title,
                                "subtitle" : subtitle,
                                "body" : body
                            },
                            "fcm_options": {
                                "image": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png"
                            }
                        }
                    }
                },
                "token": token,
                "data": {
                    "path": path,
                    "data1": data1,
                    "data2": data2
                }
            }
        }

        response = requests.post(url, headers=headers, json=data)
    
    return response

@permission_classes([IsAdminUser]) 
@api_view(['GET'])
def firebase_push(request, userId):
    title = request.query_params.get('title', os.environ.get('FIREBASE_APP_NAME'))
    subtitle = request.query_params.get('subtitle', 'Subtitle')
    body = request.query_params.get('body', 'Corpo della notifica')

    silent = request.query_params.get('silent', None)
    badge = int(request.query_params.get('badge', 0))

    data1 = request.query_params.get('data1', None)
    data2 = request.query_params.get('data2', None)
    path = request.query_params.get('path', None)

    response = send_firebase_notification(request, userId, title, subtitle, body, badge, silent, data1, data2, path, 'Default')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/default_path/'))

@permission_classes([AllowAny])
@api_view(['GET'])
def latest_app(request, platform):
    base_url=os.environ.get('NOTIFICATION_SENDER_URL')
    microservizio_url = f'{base_url}/latest_app/'
    
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
    
def _get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_PATH, scopes=SCOPES)
    
    request = google_requests.Request()
    credentials.refresh(request)
    return credentials.token
