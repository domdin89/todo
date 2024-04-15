from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

from accounts.models import Privacy, Profile
from accounts.serializers import PrivacySerializer
from accounts.views import login_without_password
from apartments.serializers import ApartmentBaseSerializer
from worksites.serializers import WorksiteSerializer
from .decorators import validate_token
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status

from django.contrib.auth.models import User
from worksites.models import CollabWorksites, Worksites
from file_manager.models import Directory
from file_manager.serializers import DirectorySerializer,DirectorySerializerNew, DirectorySerializerChildren
from apartments.models import ApartmentAccessCode, Apartments, ClientApartments
from accounts.serializers import ProfileSerializer


@api_view(['GET'])
@validate_token
def get_profile(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)

    serializer = ProfileSerializer(profile)

    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['PUT'])
@parser_classes([MultiPartParser])
@validate_token
def edit_profile(request):
    profile_id = request.profile_id
    required_fields = ['email', 'password']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        profile = Profile.objects.get(id=profile_id)

        profile.image = request.FILES.get('image', "")
        profile.first_name = request.data.get('first_name', "")
        profile.last_name = request.data.get('last_name', "")
        profile.mobile_number = request.data.get('mobile_number', "")
        profile.user.email = request.data.get('email', "")
        profile.email = request.data.get('email', "")
        img_visible = request.data.get('img_visible')
        if img_visible:
            profile.img_visible = True
        else:
            profile.img_visible = False
        email_visible = request.data.get('email_visible')
        if email_visible:
            profile.email_visible = True
        else:
            profile.email_visible = False
        phone_visible = request.data.get('phone_visible')
        if phone_visible:
            profile.phone_visible = True
        else:
            profile.phone_visible = False
       

        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password and password == confirm_password:
            profile.user.password = make_password(password)
        else:
            return Response({'message': 'Attenzione, le due password non coincidono'}, status=status.HTTP_400_BAD_REQUEST)

        profile.need_change_password = False

        profile.user.save()
        profile.save()

        return Response({'message': 'Profilo aggiornato correttamente'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@parser_classes([MultiPartParser])
@validate_token
def edit_profile_partial(request):
    profile_id = request.profile_id
    
    try:
        profile = Profile.objects.get(id=profile_id)

        profile.image = request.FILES.get('image', profile.image)
        profile.first_name = request.data.get('first_name', profile.first_name)
        profile.last_name = request.data.get('last_name', profile.last_name)
        profile.mobile_number = request.data.get('mobile_number', profile.mobile_number)
        profile.user.email = request.data.get('email', profile.user.email)
        print(f'image {profile.user.email}')

        profile.user.save()
        profile.save()

        return Response({'message': 'Profilo aggiornato correttamente'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@validate_token
def worksites(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)
    worksites = None

    if profile.type == "TECNICI" or profile.type == "STAFF":
        worksites = Worksites.objects.filter(collaborations__profile_id=profile_id, collaborations__is_valid=True).distinct()
    else:
        worksites = Worksites.objects.filter(apartments__clientapartments__profile_id=profile_id).distinct()

    serializer = WorksiteSerializer(worksites, many=True)

    return Response({'results': serializer.data})


@api_view(['GET'])
@validate_token
def apartments(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)
    worksite = request.query_params.get('worksite')
    apartments = None

    if profile.type == "TECNICI" or profile.type == "STAFF":
        apartments = Apartments.objects.filter(worksite_id=worksite,
                                               worksite__collaborations__profile_id=profile_id, 
                                               worksite__collaborations__is_valid=True, 
                                               ).distinct()
    else:
        apartments = Apartments.objects.filter(clientapartments__profile_id=profile_id, worksite_id=worksite, subs__is_valid=True).distinct()
    serializer = ApartmentBaseSerializer(apartments, many=True)

    return Response({'results': serializer.data})


@api_view(['POST'])
def apartment_code_validator(request):
    pin = request.data.get('pin')

    if pin:
        access_code = ApartmentAccessCode.objects.get(pin=pin, is_valid=True)

        if access_code.apartment:
            ClientApartments.objects.create(
                profile=access_code.profile,
                apartment=access_code.apartment,
                is_active=True,
            )            
            

        jwt_token, access_token = login_without_password(access_code.profile) # type: ignore

        if str(access_token) and str(jwt_token):
            access_code.is_valid = False
            access_code.save()
        
        return Response({
            "access": str(access_token),
            "refresh": str(jwt_token),
        })
    
@api_view(['GET'])
@validate_token
def get_directories_by_apartments(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)

    apartment_id = request.query_params.get('apartment_id')
    parent_id = request.query_params.get('parent_id')

    if not apartment_id:
        return Response({"error": "apartment_id è richiesto."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if parent_id:
            directories = Directory.objects.filter(id=parent_id)
        else:
            directories = Directory.objects.filter(apartment_id=apartment_id)

        serializer = DirectorySerializerChildren(directories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@validate_token
def get_directories(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)

    worksite_id = request.query_params.get('worksite_id')

    if not worksite_id:
        return Response({"error": "worksite_id è richiesto."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        directories = Directory.objects.filter(worksite_id=worksite_id, parent__isnull=True).distinct()
        serializer = DirectorySerializerNew(directories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def get_privacy(request):
    privacy = Privacy.objects.filter().first()
    serializer=PrivacySerializer(privacy)

    return Response(serializer.data, status=status.HTTP_200_OK)
