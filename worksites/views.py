import json
from datetime import datetime
from collections import defaultdict

from django.db.models import CharField, Count, F, Prefetch, Value as V
from django.db.models.functions import Concat
from django.forms import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.paginator import Paginator

from rest_framework import generics, mixins, serializers, status, viewsets
from rest_framework.decorators import api_view, parser_classes
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from accounts.models import Profile
from accounts.serializers import ProfileSerializer, ProfileSerializerRole
from apartments.models import ApartmentSub
from worksites.decorators import validate_token
from worksites.filters import WorksitesFilter
from .models import (Categories, CollabWorksites, FoglioParticella, Profile, Worksites, WorksitesCategories, WorksitesFoglioParticella, WorksitesProfile)
from .serializers import (CollabWorksitesNewSerializer, CollabWorksitesSerializer, CollabWorksitesSerializer2, CollaborationSerializer, CollaborationSerializerEdit, FoglioParticellaSerializer, ProfileSerializer2, WorksiteFoglioParticellaSerializer, WorksiteProfileSerializer, WorksiteSerializer, WorksiteStandardSerializer, WorksiteUserProfileSerializer)


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50

class BaseAPIView(GenericAPIView):
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = []  # Questo sarà sovrascritto nelle viste derivate per specificare i campi di ricerca
    ordering_fields = '__all__'  # Permette l'ordinamento su tutti i campi, personalizzabile nelle viste derivate
    ordering = ['id']  # Ordinamento di default, personalizzabile nelle viste derivate
    serializer_class = None  # Da impostare nella vista derivata
    queryset = None  # Da impostare nella vista derivata

    def get_queryset(self):
        """
        Sovrascrivere questo metodo nelle classi derivate per fornire il queryset specifico.
        """
        if self.queryset is not None:
            return self.queryset
        else:
            raise NotImplementedError("La vista deve definire un `queryset` o sovrascrivere `get_queryset()`")

    def get_serializer_class(self):
        """
        Sovrascrivere questo metodo nelle classi derivate per fornire il serializer specifico.
        """
        if self.serializer_class is not None:
            return self.serializer_class
        else:
            raise NotImplementedError("La vista deve definire un `serializer_class` o sovrascrivere `get_serializer_class()`")


    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        """
        Applica i filtri di backend definiti a `filter_backends`.
        """
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

class CollaboratorListView(APIView):
    pagination_class = CustomPagination

    def get_profile_count(self, worksite_id, search_query=None):
        collabs = CollabWorksites.objects.filter(worksite_id=worksite_id).select_related('profile')

        # Applicare la ricerca se presente
        if search_query:
            collabs = collabs.filter(
                Q(profile__first_name__icontains=search_query) |
                Q(profile__last_name__icontains=search_query) |
                Q(profile__mobile_number__icontains=search_query) |
                Q(profile__email__icontains=search_query)
            )

        # Estrarre gli ID dei profili unici
        profile_ids = collabs.values_list('profile__id', flat=True)

        # Counting unique profiles instead of CollabWorksites
        profile_count = Profile.objects.filter(id__in=profile_ids).distinct().count()
        return profile_count

    def get(self, request, *args, **kwargs):
        worksite_id = request.query_params.get('worksite')
        search_query = request.query_params.get('search')  # Aggiunto per la ricerca
        profile_count = self.get_profile_count(worksite_id, search_query)

        # Estrarre gli ID dei profili unici
        collabs = CollabWorksites.objects.filter(worksite_id=worksite_id).select_related('profile')
        profile_ids = collabs.values_list('profile__id', flat=True)

        # Applicare la paginazione agli ID dei profili
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(profile_ids, request)

        if page is not None:
            # Recuperare i profili paginati basandosi sugli ID
            profiles = Profile.objects.filter(id__in=page).distinct()

            # Preparare la risposta aggregata
            response_data = []
            for profile in profiles:
                collab_data = collabs.filter(profile=profile).prefetch_related(Prefetch('profile', queryset=Profile.objects.all()))
                profile_data = {
                    "profile": ProfileSerializer(profile).data,
                    "roles": CollabWorksitesSerializer(collab_data, many=True).data
                }
                response_data.append(profile_data)

            return paginator.get_paginated_response(response_data)

        return Response({"message": "No data found or invalid page number"})

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