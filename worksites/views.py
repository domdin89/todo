import json
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from accounts.serializers import ProfileSerializer, ProfileSerializerRole
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V
from django.db.models import Prefetch
from apartments.models import ApartmentSub
from worksites.decorators import validate_token
from django.http import HttpResponseBadRequest, HttpResponseServerError
from datetime import datetime
from django.db.models import F
from rest_framework import serializers, viewsets, routers, status
from collections import defaultdict

from worksites.filters import WorksitesFilter
from .models import Categories, CollabWorksites, FoglioParticella, Worksites, WorksitesCategories, WorksitesFoglioParticella, WorksitesProfile
from .serializers import CollabWorksitesNewSerializer, CollabWorksitesSerializer, CollaborationSerializer, CollaborationSerializerEdit, FoglioParticellaSerializer, WorksiteFoglioParticellaSerializer, WorksiteProfileSerializer, WorksiteSerializer, WorksiteStandardSerializer, WorksiteUserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import CollabWorksites, Profile, Worksites
from .serializers import CollaborationSerializer
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from accounts.models import Profile
from django.db.models import Count

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class BaseParams(APIView):
    pagination_class = CustomPagination
    parser_classes = []
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = []
    filterset_class = []
    serializer_class = []
    queryset = Worksites.objects.all().order_by('-id')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'search_fields' in kwargs:
            self.search_fields = kwargs['sear1ch_fields']

        if 'parser_classes' in kwargs:
            self.parser_classes = kwargs['parser_classes']

        if 'filter_class' in kwargs:
            self.filter_class = kwargs['filter_class']

        if 'serializer' in kwargs:
            self.serializer = kwargs['serializer']
        
        if 'queryset' in kwargs:
            self.queryset = kwargs['queryset']
    
    def get(self, request):
        order_param = request.GET.get('order', 'desc')
        order_by_field = request.GET.get('order_by', 'id')
        
        status = request.GET.get('status')
        if status is not None:
            try:
                status = int(status)
            except ValueError:
                return Response(status=HttpResponseBadRequest.status_code)  

            if status == 0:
                if self.queryset is None:
                    return Response(status=HttpResponseServerError.status_code)  
                serializer = self.serializer(self.queryset, many=True)
                return Response(serializer.data)
            elif status == 1:
                filtered_queryset = self.queryset.filter(is_visible=True)  
                serializer = self.serializer(filtered_queryset, many=True)
                return Response(serializer.data)
            elif status == 2:
                filtered_queryset = self.queryset.filter(is_visible=False)  
                serializer = self.serializer(filtered_queryset, many=True)
                return Response(serializer.data)
        
        if order_param == 'desc':
            queryset = self.queryset.order_by('-' + order_by_field)
        else:
            queryset = self.queryset.order_by(order_by_field)
        
        serializer = self.serializer(queryset, many=True)  # Utilizza il serializzatore
        return Response(serializer.data)
class Child(BaseParams):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_fields = ['name', 'address']
        self.queryset = Worksites.objects.all().order_by('-id')
        self.serializer = WorksiteSerializer
        self.filter_class = WorksitesFilter


@api_view(['POST'])
@parser_classes([MultiPartParser])
def WorksitePostNew(request):

    # Ottieni il file immagine
    image_file = request.FILES.get('image')

    # Crea il cantiere
    post_data = {
        'image': image_file,
        'name': request.data.get('name', None),
        'address': request.data.get('address', None),
        'lat': request.data.get('lat', 0),
        'lon': request.data.get('lon', 0),
        'is_visible': request.data.get('is_visible', None),
        'net_worth': request.data.get('net_worth', 0),
        'percentage_worth': request.data.get('percentage_worth', 0),
        'link': request.data.get('link', None),
        'date_start': request.data.get('date_start', None),
        'date_end': request.data.get('date_end', None),
        'status': request.data.get('status', None),
        'codice_commessa': request.data.get('codice_commessa', None),
        'codice_CIG': request.data.get('codice_CIG', None),
        'codice_CUP': request.data.get('codice_CUP', None),
    }

    # Rimuovi i campi vuoti o non validi
    post_data = {key: value for key, value in post_data.items() if value is not None}

    # Crea il cantiere solo se tutti i campi obbligatori sono presenti
    try:
        worksite = Worksites.objects.create(**post_data)
    except ValidationError as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    # Gestisci foglio_particelle solo se è presente
    foglio_particelle = request.data.getlist('foglio_particelle', None)
    if foglio_particelle:
        for item in foglio_particelle:
            # Converti la stringa JSON in un dizionario Python
            item_dict = json.loads(item)
            foglio_particella = FoglioParticella.objects.create(
                foglio=item_dict.get('foglio'),
                particella=item_dict.get('particella')
            )

            WorksitesFoglioParticella.objects.create(
                foglio_particella=foglio_particella,
                worksite=worksite
            )

    return Response('tutto regolare', status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def new_category(request, worksite_id=None):

    # Ottieni il file immagine
    category = request.data.get('category')

    Categories.objects.create(
        name=category
    )

    if worksite_id:
        WorksitesCategories.objects.create(
            worksite=Worksites.objects.get(id=worksite_id),
            category=category
        )

    return Response('tutto regolare', status=status.HTTP_200_OK)

        
@api_view(['PUT'])
@parser_classes([MultiPartParser])
def update_worksite(request, worksite_id):  # Aggiunta dell'argomento worksite_id
    try:
        worksite = Worksites.objects.get(id=worksite_id)
    except Worksites.DoesNotExist:
        return Response("Cantiere non trovato", status=status.HTTP_404_NOT_FOUND)

    post_data = {
        'name': request.data.get('name', worksite.name),
        'address': request.data.get('address', worksite.address),
        'lat': request.data.get('lat', worksite.lat),
        'lon': request.data.get('lon', worksite.lon),
        'is_visible': request.data.get('is_visible', worksite.is_visible),
        'net_worth': request.data.get('net_worth', worksite.net_worth),
        'image': request.FILES.get('image', worksite.image),
        'percentage_worth': request.data.get('percentage_worth', worksite.percentage_worth),
        'link': request.data.get('link', worksite.link),
        'date_start': request.data.get('date_start', worksite.date_start),
        'date_end': request.data.get('date_end', worksite.date_end),
        'status': request.data.get('status', worksite.status),
        'codice_commessa': request.data.get('codice_commessa', worksite.codice_commessa),
        'codice_CIG': request.data.get('codice_CIG', worksite.codice_CIG),
        'codice_CUP': request.data.get('codice_CUP', worksite.codice_CUP),
    }

    # Rimuovi i campi vuoti o non validi
    post_data = {key: value for key, value in post_data.items() if value is not None}

    # Aggiorna i campi del cantiere
    for key, value in post_data.items():
        setattr(worksite, key, value)

    # Salva il cantiere
    worksite.save()

    return Response("Cantiere aggiornato con successo", status=status.HTTP_200_OK)


           
@api_view(['PUT'])
def update_foglio_particella(request, id):
    try:
        worksite_foglio_particella = WorksitesFoglioParticella.objects.get(id=id)
        foglio_particella = worksite_foglio_particella.foglio_particella
    except WorksitesFoglioParticella.DoesNotExist:  # Fixing the exception type
        return Response("Foglio Particella non trovato", status=status.HTTP_404_NOT_FOUND)

    if foglio_particella:
        foglio_particelle = request.data.getlist('foglio_particelle', foglio_particella)
        for item in foglio_particelle:
            # Convert the JSON string to a Python dictionary
            item_dict = json.loads(item)
            # Assuming foglio_particella is an instance of a model with fields foglio and particella
            foglio_particella.foglio = item_dict.get('foglio')
            foglio_particella.particella = item_dict.get('particella')
            
            foglio_particella.save()


    return Response("Foglio_particella aggiunta con successo", status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_categories(request, id):
    try:
        worksite_category = WorksitesCategories.objects.get(id=id)
        category = worksite_category.category
    except WorksitesCategories.DoesNotExist:  # Fixing the exception type
        return Response("Categoria non trovata", status=status.HTTP_404_NOT_FOUND)

    if category:
        categories = request.data.getlist('categories', category)  # Fixing variable name
        for item in categories:
            # Convert the JSON string to a Python dictionary
            item_dict = json.loads(item)
            # Assuming category is an instance of a model with a field 'name'
            category.name = item_dict.get('name')
            
            category.save()

    return Response("Categoria aggiornata con successo", status=status.HTTP_200_OK)


@api_view(['PUT'])
def edit_worksite_foglio_particella(request, worksite_foglio_particella_id, foglio_particella_id, worksite):
    worksite_foglio_particella = WorksitesFoglioParticella.objects.get(pk=worksite_foglio_particella_id)
    foglio_particella = FoglioParticella.objects.get(pk=foglio_particella_id)
    worksite_get = Worksites.objects.get(pk=worksite)

    try:
        worksite_foglio_particella.foglio_particella = foglio_particella
        worksite_foglio_particella.worksite = worksite_get


        worksite_foglio_particella.save()


    except:
            return Response('foglio particella errato', status=status.HTTP_400_BAD_REQUEST)

    return Response("Foglio_particella aggiunta con successo", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_worksite(request, id):
    try:
        worksite = Worksites.objects.get(id=id)
    except Worksites.DoesNotExist:
        return Response("Worksite non trovato", status=status.HTTP_404_NOT_FOUND)

    worksite.is_active = False
    worksite.save()

    return Response("Worksite rimosso", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_category(request, id):
    try:
        worksite_category = WorksitesCategories.objects.get(id=id)
    except WorksitesCategories.DoesNotExist:
        return Response("Categoria non trovata", status=status.HTTP_404_NOT_FOUND)

    worksite_category.delete()

    return Response("Relazione Categoria eliminata e Worksite rimosso", status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_foglio_particella(request, id):
    try:
        worksite_foglio_particella = WorksitesFoglioParticella.objects.get(id=id)
    except WorksitesFoglioParticella.DoesNotExist:
        return Response("WorksitesFoglioParticella non trovato", status=status.HTTP_404_NOT_FOUND)

    foglio_particella = worksite_foglio_particella.foglio_particella

    try:
        subs = ApartmentSub.objects.filter(foglio_particella=foglio_particella)
        for sub in subs:
            sub.foglio_particella = None  # Rimuovi il collegamento a FoglioParticella
            sub.save()
    except ApartmentSub.DoesNotExist:
        pass

    worksite_foglio_particella.delete()

    return Response("Relazione WorksitesFoglioParticella eliminata e collegamenti ApartmentSubs correlati rimossi", status=status.HTTP_200_OK)



class WorksiteListView(ListAPIView):
    queryset = Worksites.objects.filter(is_active=True)
    serializer_class = WorksiteSerializer
    #permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filterset_class = WorksitesFilter
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        status = self.request.GET.get('status', None)
        
        if status is not None:
            try:
                status = int(status)
            except ValueError:
                return queryset.none()  # Return an empty queryset if status is invalid
            
            if status == 0:
                return queryset
            elif status == 1:
                return queryset.filter(is_open=True)
            elif status == 2:
                return queryset.filter(is_open=False)

        return queryset

class WorksiteDetail(RetrieveUpdateAPIView):
    queryset = Worksites.objects.filter(is_active=True)
    serializer_class = WorksiteSerializer
    lookup_field = 'pk'
    parser_classes = (MultiPartParser, FormParser)  # Utilizza il parser multipart/form-data

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=self.kwargs.get('partial', False))
        if serializer.is_valid():
            self.perform_update(serializer)
        return Response(serializer.data)

class CollaboratorListView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request):
        worksite_id = request.GET.get('worksite')
        if not worksite_id:
            raise Http404("Il parametro 'worksite' è obbligatorio.")

        order_param = request.GET.get('order', 'desc')
        order_by_field = request.GET.get('order_by', 'id')

        # Ottieni i CollabWorksites per il worksite specificato
        collab_worksites = CollabWorksites.objects.filter(worksite_id=worksite_id)

        # Dizionario per memorizzare i profili con i rispettivi ruoli
        profile_roles = defaultdict(list)

        # Popola il dizionario
        for collab_worksite in collab_worksites:
            profile = collab_worksite.profile
            profile_data = {
                'id': profile.id,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'email': profile.email,
                'mobile_number': profile.mobile_number,
                'image': profile.image.url if profile.image else None,  # Se l'attributo 'image' non esiste, restituisce None
            }
            
            # worksite_serializer = WorksiteStandardSerializer(collab_worksite.worksite)
            # worksite_data = worksite_serializer.data
            # profile_roles[profile.id].append(worksite_data)

            collab_worksite_serializer = CollabWorksitesSerializer(collab_worksite)
            collab_worksite_data = collab_worksite_serializer.data
            profile_roles[profile.id].append(collab_worksite_data)

        
        print(profile_roles.items())

        # Costruisci la risposta
        data = []
        for profile_id, roles in profile_roles.items():
            profile_data = {
                'profile': {
                    'id': profile_id,
                    'first_name': profile_data.get('first_name', ''),  # Utilizza il metodo get per ottenere il valore, se non presente restituisce una stringa vuota
                    'last_name': profile_data.get('last_name', ''),  # Se è None, sostituisci con stringa vuota
                    'email': profile_data.get('email', ''),
                    'mobile_number': profile_data.get('mobile_number', ''),
                    'image': profile_data.get('image', ''),
                },
               
                'roles': roles
            }
            data.append(profile_data)

        # Pagina i dati
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(data, request)
        
        return paginator.get_paginated_response(result_page)
       

    # def post(self, request, *args, **kwargs):
    #     profile_id = request.data.get('profile')
    #     worksite_id = request.data.get('worksite')
    #     role = request.data.get('role')
    #     order = request.data.get('order')

    #     profile = get_object_or_404(Profile, id=profile_id)
    #     worksite = get_object_or_404(Worksites, id=worksite_id)

    #     collab_worksite = CollabWorksites.objects.create(
    #         profile=profile,
    #         worksite=worksite,
    #         role=role,
    #         order=order
    #     )

    #     serializer = self.get_serializer(collab_worksite)
    #     return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
    

    

class CollaboratorUpdateView(RetrieveUpdateAPIView):
    queryset = CollabWorksites.objects.all()
    serializer_class = CollaborationSerializerEdit
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

@api_view(['DELETE'])
def delete_collaborator(request, id):
    try:
        collaborator = CollabWorksites.objects.get(id=id)
    except CollabWorksites.DoesNotExist:
        return Response("Collaboratore non trovato", status=status.HTTP_404_NOT_FOUND)

    collaborator.date_end = datetime.now()
    collaborator.save()

    return Response("Collaboratore rimosso", status=status.HTTP_200_OK)


class WorksiteProfileListView(ListCreateAPIView):
    serializer_class = WorksiteProfileSerializer
    #permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['profile__first_name', 'profile__last_name', 'worksite__name']

    def get_queryset(self):
        queryset = CollabWorksites.objects.all()
        worksite_id = self.request.GET.get('worksite')
        role = self.request.GET.get('role')
        order_param = self.request.GET.get('order', 'desc')
        order_by_field = self.request.GET.get('order_by', 'id')  # Prendi il campo da 'order_by', default a 'id'
        
        # Applica direttamente l'ordinamento
        if order_param == 'desc':
            queryset = queryset.order_by('-' + order_by_field)  # Ordinamento discendente
        else:
            queryset = queryset.order_by(order_by_field)  # Ordinamento ascendente

        if worksite_id:
            queryset = queryset.filter(worksite__id=worksite_id)
        
        if role:
            queryset = queryset.filter(profile__type=role)

        # Implementing search functionality through the filter_backends
        return queryset
    

class WorksiteProfileUserListView(ListCreateAPIView):
    serializer_class = WorksiteUserProfileSerializer
    #permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['profile__first_name', 'profile__last_name']

    def get_queryset(self):
        worksite_id = self.request.GET.get('worksite')
        queryset = WorksitesProfile.objects.filter(worksite_id=worksite_id, profile__type='USER')
        order_param = self.request.GET.get('order', 'desc')
        order_by_field = self.request.GET.get('order_by', 'id')  # Prendi il campo da 'order_by', default a 'id'
        
        # Applica direttamente l'ordinamento
        if order_param == 'desc':
            queryset = queryset.order_by('-' + order_by_field)  # Ordinamento discendente
        else:
            queryset = queryset.order_by(order_by_field)  # Ordinamento ascendente

        if worksite_id:
            queryset = queryset.filter(worksite__id=worksite_id)

        # Implementing search functionality through the filter_backends
        return queryset


class TechnicianNotInWorksiteView(ListAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer  # Usa il serializer appropriato per Profile

    def get_queryset(self):
        # Seleziona tutti i profili di tipo 'TECNICI'
        queryset = Profile.objects.filter(type='TECNICI')
        
        # Recupera il parametro 'worksite' dalla richiesta
        worksite_id = self.request.GET.get('worksite')
        
        if worksite_id is not None:
            # Recupera gli ID dei profili associati al worksite specificato
            associated_technician_ids = CollabWorksites.objects.filter(
                worksite_id=worksite_id
            ).values_list('profile__id', flat=True)
            
            print(f'Associated technician IDs: {associated_technician_ids}')
            
            # Esclude i tecnici associati al worksite specificato
            queryset = queryset.exclude(id__in=associated_technician_ids)
            
            print(f'Queryset after exclusion: {queryset}')
        
        return queryset