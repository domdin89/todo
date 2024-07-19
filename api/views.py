import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from accounts.models import Privacy, Profile
from accounts.serializers import PrivacySerializer
from accounts.views import login_without_password
from apartments.serializers import ApartmentBaseSerializer
from worksites.serializers import WbsSerializer, WorksiteSerializer, WorksiteDetailSerializer, ApartmentSubSerializer, ApartmentSerializer
from worksites.views import is_valid_date
from .decorators import validate_token
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from worksites.models import CollabWorksites, Contractor, Financier, FoglioParticella, Worksites, WorksitesFoglioParticella
from file_manager.models import Directory, File
from file_manager.serializers import DirectorySerializer, DirectorySerializerChildrenAppStaff,DirectorySerializerNew, DirectorySerializerChildrenApp, DirectorySerializerNewStaff
from apartments.models import WBS, ApartmentAccessCode, ApartmentSub, Apartments, ClientApartments

from accounts.serializers import ProfileSerializer
from board.models import Boards
from board.serializers import BoardsSerializer
from django.db.models import Q, Prefetch
from django.contrib.auth import authenticate
import random
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.db import transaction
import requests




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

        access_code = ApartmentAccessCode.objects.filter(profile=profile, is_valid=True).first()

        profile.image = request.FILES.get('image', "")
        profile.first_name = request.data.get('first_name', "")
        profile.last_name = request.data.get('last_name', "")
        profile.mobile_number = request.data.get('mobile_number', "")
        profile.user.email = request.data.get('email', "") # type: ignore
        profile.email = request.data.get('email', "")
        img_visible = request.data.get('img_visible')
        if img_visible == 'true':
            profile.img_visible = True
        else:
            profile.img_visible = False
        email_visible = request.data.get('email_visible')
        if email_visible == 'true':
            profile.email_visible = True
        else:
            profile.email_visible = False
        phone_visible = request.data.get('phone_visible')
        if phone_visible == 'true':
            profile.phone_visible = True
        else:
            profile.phone_visible = False
       

        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password and password == confirm_password:
            profile.user.password = make_password(password) # type: ignore
        else:
            return Response({'message': 'Attenzione, le due password non coincidono'}, status=status.HTTP_400_BAD_REQUEST)

        profile.need_change_password = False
        access_code.is_valid = False # type: ignore
        access_code.save() # type: ignore
        profile.user.save() # type: ignore
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
        profile.user.email = request.data.get('email', profile.user.email) # type: ignore
        profile.email = request.data.get('email', profile.user.email) # type: ignore
        img_visible = request.data.get('img_visible')
        if img_visible == 'true':
            profile.img_visible = True
        else:
            profile.img_visible = False
        email_visible = request.data.get('email_visible')
        if email_visible  == 'true':
            profile.email_visible = True
        else:
            profile.email_visible = False
        phone_visible = request.data.get('phone_visible')
        if phone_visible  == 'true':
            profile.phone_visible = True
        else:
            profile.phone_visible = False

        profile.user.save() # type: ignore
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
        worksites = Worksites.objects.filter(collaborations__profile_id=profile_id, collaborations__is_valid=True).order_by('-date_start').distinct()
    else:
        worksites = Worksites.objects.filter(apartments__clientapartments__profile_id=profile_id).order_by('-date_start').distinct()

    serializer = WorksiteSerializer(worksites, many=True)

    return Response({'results': serializer.data})


@api_view(['GET'])
@validate_token
def worksite_detail(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)
    worksite_id = request.query_params.get('worksite')


    if profile.type == "STAFF":
        worksites = Worksites.objects.get(id=worksite_id, collaborations__profile_id=profile_id, collaborations__is_valid=True)
    else:
        return Response({'results': '[]'})

    serializer = WorksiteDetailSerializer(worksites)

    return Response({'results': serializer.data})

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class ApartmentListViewApp(APIView):
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order_by = '-id'
        worksite_id = request.query_params.get('worksite')
        search_query = request.query_params.get('search')
        order_param = self.request.GET.get('order', 'desc')
        order_by_field = self.request.GET.get('order_by', 'id')

        if order_param == 'desc':
            order_by = '-' + order_by_field
        else:
            order_by = order_by_field


        query_params = Q() 

        if search_query:
            query_params &= Q(apartment__owner__icontains=search_query) | Q(apartment__note__icontains=search_query) | Q(sub__icontains=search_query)
        query_params &= Q(apartment__worksite_id=worksite_id,
                            is_valid=True,
                            apartment__is_active=True)

        queryset = ApartmentSub.objects.filter(
          query_params
        ).select_related('apartment').distinct()
        
        apartment_ids = queryset.values_list('apartment__id', flat=True)

        # Applicare la paginazione agli ID dei profili
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(apartment_ids, request)

        if page is not None:
            # Recuperare i profili paginati basandosi sugli ID
            apartments = Apartments.objects.filter(id__in=page).distinct().order_by(order_by)

            # Preparare la risposta aggregata
            response_data = []
            for apartment in apartments:
                apartment_data = queryset.filter(apartment=apartment).prefetch_related(Prefetch('apartment', queryset=Apartments.objects.all()))
                apartments_data = {
                    "apartments": ApartmentSerializer(apartment).data,
                    "subs": ApartmentSubSerializer(apartment_data, many=True).data,
                }
                response_data.append(apartments_data)

            return paginator.get_paginated_response(response_data)

        return Response({"message": "No data found or invalid page number"})

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
                                               is_active=True
                                               ).distinct()
    else:
        apartments = Apartments.objects.filter(clientapartments__profile_id=profile_id, worksite_id=worksite, subs__is_valid=True, is_active=True).distinct()
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

        profile = access_code.profile
        serializer = ProfileSerializer(profile)

        # if str(access_token) and str(jwt_token):
        #     access_code.is_valid = False
        #     access_code.save()
        
        return Response({
            "access": str(access_token),
            "refresh": str(jwt_token),
            "profile": serializer.data
        })
    
@api_view(['GET'])
@validate_token
def get_directories_by_apartments(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)
    directories = None

    apartment_id = request.query_params.get('apartment_id')
    parent_id = request.query_params.get('parent_id')

    if not apartment_id:
        return Response({"error": "apartment_id è richiesto."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        apartment = Apartments.objects.get(id=apartment_id)

    try:
        if parent_id:
            directories = Directory.objects.filter(id=parent_id, apartment_id=apartment_id)
        else:
            directories = Directory.objects.filter(apartment_id=apartment_id)
            if not directories:
                parent = Directory.objects.filter(worksite=apartment.worksite, apartment__isnull=True, parent__isnull=True).first()
                Directory.objects.create(
                    parent=parent,
                    apartment_id=apartment_id,
                    name=apartment.note
                )
                directories = Directory.objects.filter(apartment_id=apartment_id)
                


        if profile.type == 'STAFF':
            serializer = DirectorySerializerChildrenAppStaff(directories, many=True)
        else:
            serializer = DirectorySerializerChildrenApp(directories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@validate_token
def get_directories(request):

    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)

    worksite_id = request.query_params.get('worksite_id')
    parent_id = request.query_params.get('parent_id')

    if not worksite_id:
        return Response({"error": "worksite_id è richiesto."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if parent_id:
            directories = Directory.objects.filter(worksite_id=worksite_id, id=parent_id, apartment__isnull=True)
        else:
            directories = Directory.objects.filter(worksite_id=worksite_id, apartment__isnull=True).distinct()
        
        if profile.type == 'STAFF':
            serializer = DirectorySerializerNewStaff(directories, many=True)
        else:
            serializer = DirectorySerializerNew(directories, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_privacy(request):
    privacy = Privacy.objects.filter().first()
    serializer=PrivacySerializer(privacy)

    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@validate_token
def boards(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)


    boards = Boards.objects.filter(
        Q(recipients__apartment__clientapartments__profile=profile) | 
        Q(recipients__worksites__apartments__clientapartments__profile=profile) |
        Q(recipients__profile=profile)
    ).distinct().order_by('-date')

    serializer = BoardsSerializer(boards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        pin = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        mobile_number = request.data.get('mobile_number', None)
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response({"message": "Attenzione, le due password devono coincidere"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email, is_active=True).exists():
        # L'email esiste già nel database, gestisci di conseguenza (ad esempio, mostra un messaggio di errore)
            return Response({"message": "Attenzione, email già presente"}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=email, is_active=False).exists():
            user = User.objects.filter(email=email, is_active=False).first()
            profile = Profile.objects.filter(user_id=user.id).first() # type: ignore
            send_link(request, profile, profile.token) # type: ignore

            return Response({"message": "Token reinviato con successo"}, status=status.HTTP_200_OK)
        else:
            user = User.objects.create_user(username=email, email=email, is_active=False)
            # Set the password for the user
            user.set_password(password)
            user.save()
        
            # Create a Profile object
            profile = Profile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                mobile_number=mobile_number,
                token=pin,
                need_change_password=False,
                type = 'USER'
            )

            send_link(request, profile, pin)

        # Return a success response
            return Response({"message": "Profilo creato con successo"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Invalid request method."}, status=status.HTTP_400_BAD_REQUEST)


def send_link(request, profile, pin):
    context = {
        'token': pin,
        'profile': profile
    }
    message_txt = render_to_string('accounts/auth/registration-link.txt', context)
    message_html = render_to_string('accounts/auth/registration-link.html', context)

    prova = send_mail(
        subject='Falone conferma account',
        message=message_txt,
        html_message=message_html,
        from_email=settings.EMAIL_SENDER,  # Inserisci qui l'indirizzo email del mittente
        recipient_list=[profile.user.email],  # Inserisci qui l'indirizzo email del destinatario
        fail_silently=False,
    )

    return Response({'message': 'ok'})

@api_view(['POST'])
def confirm_account(request):
    token = request.data.get('token')

    try:
        profile = Profile.objects.filter(token=token, user__is_active=False).first()
        profile.token = None # type: ignore
        user = profile.user # type: ignore
        user.is_active = True # type: ignore
        user.save() # type: ignore
        profile.save() # type: ignore

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return Response({
            "access": str(access_token),
            "refresh": str(refresh_token)
        }, status=status.HTTP_200_OK)

    except Profile.DoesNotExist:
        return Response({"message": "Attenzione, pin non corretto"}, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['POST'])
@validate_token
def delete_account(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)
    profile.is_active = True

    profile.save()

    return Response({'message': 'account cancellato con successo'})

@api_view(['PUT'])
@parser_classes([MultiPartParser])
@validate_token
def update_worksite(request, worksite_id):

    try:
        worksite = Worksites.objects.get(id=worksite_id)
    except Worksites.DoesNotExist:
        return Response("Cantiere non trovato", status=status.HTTP_404_NOT_FOUND)

    with transaction.atomic():

        financier = request.data.get('financier', worksite.financier)
        contractor = request.data.get('contractor', worksite.contractor)
        new_financer = None
        new_contractor = None

        if financier:
            try:
                new_financer = Financier.objects.create(name=financier)
            except json.JSONDecodeError as e:
                return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
            
        if contractor:
            try:
                new_contractor = Contractor.objects.create(name=contractor)
            except json.JSONDecodeError as e:
                return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
        date_end = request.data.get('date_end')
        if not is_valid_date(date_end):
            date_end = None

        post_data = {
            'name': request.data.get('name', worksite.name),
            'address': request.data.get('address', worksite.address),
            'lat': request.data.get('lat', worksite.lat),
            'lon': request.data.get('lon', worksite.lon),
            'is_visible': True if request.data.get('is_visible', worksite.is_visible) == 'true' else False,
            'net_worth': request.data.get('net_worth', worksite.net_worth),
            'image': request.FILES.get('image', worksite.image),
            'percentage_worth': request.data.get('percentage_worth', worksite.percentage_worth),
            'link': request.data.get('link', worksite.link),
            'date_start': request.data.get('date_start', worksite.date_start),
            'date_end': date_end,
            'status': request.data.get('status', worksite.status),
            'codice_commessa': request.data.get('codice_commessa', worksite.codice_commessa),
            'codice_CIG': request.data.get('codice_CIG', worksite.codice_CIG),
            'codice_CUP': request.data.get('codice_CUP', worksite.codice_CUP),
            'financier': new_financer,
            'contractor': new_contractor
        }

        # Rimuovi i campi vuoti o non validi
        #post_data = {key: value for key, value in post_data.items() if value is not None}

        # Aggiorna i campi del cantiere
        for key, value in post_data.items():
            setattr(worksite, key, value)

        # Salva il cantiere
        worksite.save()

    return Response("Cantiere aggiornato con successo", status=status.HTTP_200_OK)

@api_view(['POST'])
@validate_token
def directory_new(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)
    name = request.data.get('name')
    parent_id = request.data.get('parent_id', None)

    if not name:
        return JsonResponse({'error': 'Il nome della cartella è obbligatorio.'}, status=400)
    
    # Crea la cartella (directory)
    try:
        if parent_id:
            parent = Directory.objects.get(id=parent_id)
            if parent.apartment:
                directory = Directory.objects.create(created_by=profile, name=name, parent=parent, apartment=parent.apartment)
            elif parent.worksite:
                directory = Directory.objects.create(created_by=profile, name=name, parent=parent, worksite=parent.worksite)
            else:
                directory = Directory.objects.create(created_by=profile, name=name, parent=parent)
        else:
            directory = Directory.objects.create(created_by=profile, name=name)
        return JsonResponse({'message': 'Cartella creata con successo.', 'id': directory.id}, status=201) # type: ignore
    except Directory.DoesNotExist:
        return JsonResponse({'error': 'Cartella parent non trovata.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@api_view(['POST'])
@validate_token
def file_visible(request):
    profile_id = request.profile_id
    profile = Profile.objects.get(id=profile_id)
    file_id = request.data.get('file_id')
    file_visibility = request.data.get('file_visibility')


    if profile.type == 'STAFF':
        file = File.objects.get(id=file_id)
        file.visible_in_app = file_visibility == 'true'
        file.da_visionare = False
        file.save()
       
    return JsonResponse({'message': 'Visibilità modificata con successo'}, status=200)
    
    
@api_view(['POST'])
@parser_classes([MultiPartParser])
@validate_token
def file_new(request):
    directory_id = request.data.get('directory_id')
    name = request.data.get('name', None)
    file = request.data.get('file', None)

    if not name or not directory_id:
        return JsonResponse({'error': 'Il nome della cartella e il parent id sono obbligatori.'}, status=400)
    
    try:
        file_new = File.objects.create(name=name, directory_id=directory_id, file=file, visible_in_app=False)
        return JsonResponse({'message': 'File caricato con successo.', 'file': file_new.id}, status=201) # type: ignore
    except Directory.DoesNotExist:
        return JsonResponse({'error': 'File non trovato.'}, status=404)

def create_tinyurl(request, url):
    if request.method == 'POST':
        api_token = '4UEg0RmH3QcYDpVak9OImrePpnDtNU2Qe6wPU1abikgzPnfehbHFvbNJlcwL'
        url = url
        domain = 'tinyurl.com'

        if not url:
            return Response({'error': 'URL is missing'})

        try:
            # Make a POST request to the TinyURL API
            api_url = f'https://api.tinyurl.com/create?api_token={api_token}'
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            data = {
                'url': url,
                'domain': domain
            }
            response = requests.post(api_url, headers=headers, json=data)
            response_data = response.json()

            # Check if the response contains the shortened URL
            if 'data' in response_data and 'tiny_url' in response_data['data']:
                tinyurl = response_data['data']['tiny_url']
                return tinyurl
            else:
                return Response({'error': 'Failed to create TinyURL'})

        except requests.exceptions.RequestException as e:
            return Response({'error': 'Failed to connect to TinyURL service'})

    return Response({'error': 'Invalid request method'})

@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    profile = get_object_or_404(Profile, email=email)

    reset_token = default_token_generator.make_token(profile.user)
    uid = urlsafe_base64_encode(force_bytes(profile.pk))

    reset_link = f'https://falone-test.falone.madstudio.it/auth/amplify/forgot-password?uid={uid}&reset_token={reset_token}'
    #reset_link = f'http://localhost:8080/auth/amplify/forgot-password?uid={uid}&reset_token={reset_token}'


    #shortened_url = create_tinyurl(request, reset_link)

    send_reset_email(profile, reset_link)


    return Response({
                    'message': 'Link ripristino password inviato per email'
                     }, status=status.HTTP_200_OK)


@api_view(['POST'])
def password_reset_confirm(request):
    try:
        uidb64 = request.data.get('uid')
        token = request.data.get('reset_token')
        uid = force_str(urlsafe_base64_decode(uidb64))
        profile = Profile.objects.get(pk=uid)

        user = profile.user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({
                    'message': "Attenzione, utente non trovato"
                     }, status=status.HTTP_404_NOT_FOUND)

    if default_token_generator.check_token(user, token):
        # Handle the password reset here
        # For example, you can update the user's password and log them in.
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({'message': 'Attenzione, le due password non coincidono'})
        else:
            user.set_password(new_password) # type: ignore

        user.save() # type: ignore
        return Response({
                    'message': 'Password modificata con successo'
                     }, status=status.HTTP_200_OK)
    else:
        return Response({
                    'message': "Attenzione, token non corretto"
                     }, status=status.HTTP_403_FORBIDDEN)

def send_reset_email(user, reset_link):
    context = {
        'reset_link': reset_link,
    }
    message_txt = render_to_string('password_reset_link.txt', context)
    
    message_html = render_to_string('password_reset_link.html', context)
    print(message_html)

    send_mail(
        subject='Password Reset',
        message=message_txt,
        html_message=message_html,
        from_email=settings.EMAIL_SENDER,
        recipient_list=[user.email],
        fail_silently=False,
    )
