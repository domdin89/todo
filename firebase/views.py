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

@permission_classes([IsAdminUser]) 
@api_view(['GET'])
def latest_app(request, platform):
    version = LastVersion.objects.get(platform=platform)
    serializer = LastVersionSerializer(version, many=False)
    return Response(serializer.data)
