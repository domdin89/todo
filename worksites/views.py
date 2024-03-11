import json
from datetime import datetime
from collections import defaultdict

from django.db.models import CharField, Count, F, Prefetch, Value as V
from django.db.models.functions import Concat
from django.forms import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Min

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
from django.db import connection
from django.db.models import Q
from django.db import IntegrityError
from django.db.utils import IntegrityError
from django.db.models import Max


from accounts.models import Profile
from accounts.serializers import ProfileSerializer, ProfileSerializerRole
from apartments.models import ApartmentSub, Apartments
from worksites.decorators import validate_token
from worksites.filters import WorksitesFilter
from .models import (Categories, CollabWorksites, CollabWorksitesOrder, FoglioParticella, Profile, Status, Worksites, WorksitesCategories, WorksitesFoglioParticella, WorksitesProfile, WorksitesStatus)
from .serializers import (ApartmentSerializer, ApartmentSubSerializer, CollabWorksitesNewSerializer, CollabWorksitesOrderSerializer, CollabWorksitesSerializer, CollabWorksitesSerializer2, CollaborationSerializer, CollaborationSerializerEdit, FoglioParticellaSerializer, ProfileSerializer2, ProfileSerializerPD, StatusSerializer, WorksiteFoglioParticellaSerializer, WorksiteProfileSerializer, WorksiteSerializer, WorksiteStandardSerializer, WorksiteStatusSerializer, WorksiteUserProfileSerializer)


# def prova(request):
    
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT VERSION()")
#         row = cursor.fetchone()
#         if row is not None:
#             version = row[0]
#         else:
#             version = "N/D"  # Versione non disponibile
#     return JsonResponse({'mysql_version': version})



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
        collabs = CollabWorksitesOrder.objects.filter(worksite_id=worksite_id, is_valid=True).select_related('profile')

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
        search_query = request.query_params.get('search')
        #profile_count = self.get_profile_count(worksite_id, search_query)

        search_filters = Q()

        if search_query:
            search_filters |= Q(profile__first_name__icontains=search_query)
            search_filters |= Q(profile__last_name__icontains=search_query)
            search_filters |= Q(profile__mobile_number__icontains=search_query)
            search_filters |= Q(profile__email__icontains=search_query)


        collabs = CollabWorksitesOrder.objects.filter(
            search_filters,
            worksite_id=worksite_id,
            is_valid=True
        ).select_related('profile').distinct()

        collabs = collabs.order_by('order')

        profile_ids = collabs.values_list('profile__id', flat=True)


        # Applicare la paginazione agli ID dei profili
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(profile_ids, request)

        if page is not None:
             serializer = CollabWorksitesOrderSerializer(collabs, many=True)

             return paginator.get_paginated_response(serializer.data)
           

        return Response({"message": "No data found or invalid page number"})
    


class ApartmentListView(APIView):
    pagination_class = CustomPagination

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
            query_params &= Q(apartment__owner__icontains=search_query) | Q(apartment__note__icontains=search_query)
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


@api_view(['POST'])
def new_collabworksite(request):
    roles = request.data.get('roles', [])
    order = request.data.get('order', None)
    profile_id = request.data.get('profile', None)
    worksite_id= request.data.get('worksite', None)

    for role in roles:
        post_data = {
            'profile_id': profile_id,
            'worksite_id': worksite_id,
            'role': role.get('role'),
        }

        post_data = {key: value for key, value in post_data.items() if value is not None}

        try:
            CollabWorksites.objects.create(**post_data)
        except IntegrityError as e:
            # Qui catturiamo l'IntegrityError e restituiamo un messaggio di errore personalizzato
            return Response({'error': 'Errore di integrità dei dati. Assicurati che il profile_id e il worksite_id siano validi e esistenti.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    

    CollabWorksitesOrder.objects.create(
        order = order,
        profile_id = profile_id,
        worksite_id= worksite_id
    )
    return Response('tutto regolare', status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_collabworksite(request):
    profile = request.data.get('profile')
    worksite = request.data.get('worksite')
    roles = request.data.get('roles', [])


    collaborators = CollabWorksites.objects.filter(worksite_id=worksite, profile_id=profile)

    for collaborator in collaborators:
        collaborator.is_valid = False
        collaborator.save()

    for role in roles:
        post_data = {
            'profile_id': request.data.get('profile', None),
            'worksite_id': request.data.get('worksite', None),
            'order': role.get('order'),
            'role': role.get('role'),
        }

        post_data = {key: value for key, value in post_data.items() if value is not None}

        try:
            CollabWorksites.objects.create(**post_data)
        except IntegrityError as e:
            # Qui catturiamo l'IntegrityError e restituiamo un messaggio di errore personalizzato
            return Response({'error': 'Errore di integrità dei dati. Assicurati che il profile_id e il worksite_id siano validi e esistenti.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response('tutto regolare', status=status.HTTP_200_OK)

@api_view(['PUT'])
def delete_collabworksite(request):
    profile = request.data.get('profile')
    worksite = request.data.get('worksite')


    collaborators = CollabWorksites.objects.filter(worksite_id=worksite, profile_id=profile)
    collaborators_order = CollabWorksitesOrder.objects.filter(worksite_id=worksite, profile_id=profile)

    for collaborator in collaborators:
        collaborator.is_valid = False
        collaborator.save()

    for collaborator in collaborators_order:
        collaborator.is_valid = False
        collaborator.save()

    return Response('tutto regolare', status=status.HTTP_200_OK)



@api_view(['POST'])
@parser_classes([MultiPartParser])
def WorksitePostNew(request):

    # Ottieni il file immagine
    image_file = request.FILES.get('image')
    is_visible = request.data.get('is_visible', None),

    # Crea il cantiere
    post_data = {
        'image': image_file,
        'name': request.data.get('name', None),
        'address': request.data.get('address', None),
        'lat': request.data.get('lat', 0),
        'lon': request.data.get('lon', 0),
        'is_visible': is_visible == 'true',
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
    serializer_class = ProfileSerializerPD  # Usa il serializer appropriato per Profile

    def get_queryset(self):
        # Seleziona tutti i profili di tipo 'TECNICI'
        queryset = Profile.objects.filter(type='TECNICI')
        
        # Recupera il parametro 'worksite' dalla richiesta
        worksite_id = self.request.GET.get('worksite')
        
        if worksite_id is not None:
            # Recupera gli ID dei profili associati al worksite specificato
            associated_technician_ids = CollabWorksitesOrder.objects.filter(
                worksite_id=worksite_id,
                is_valid=True
            ).values_list('profile__id', flat=True)
            
            
            # Esclude i tecnici associati al worksite specificato
            queryset = queryset.exclude(id__in=associated_technician_ids)
            
        
        return queryset
    

@api_view(['GET'])
def get_worksite_status(request, id):
    # Ottieni tutti gli status ordinati
    statuses = Status.objects.all().order_by('order')
    
    # Prepariamo la lista dei dati finali
    statuses_data = []

    # Per ogni status, trova il WorksiteStatus attivo associato
    for status in statuses:
        # Cerca il WorksitesStatus attivo per il dato status e worksite
        active_status = WorksitesStatus.objects.filter(
            status=status, 
            worksite_id=id, 
            active=True
        ).first()

        # Serializza lo status e aggiungi i dati del WorksitesStatus attivo
        status_data = StatusSerializer(status).data
        status_data['active'] = WorksiteStatusSerializer(active_status).data if active_status else None
        statuses_data.append(status_data)

    return Response(statuses_data)

@api_view(['POST'])
def update_worksite_status(request):

    worksite_id = request.data.get('worksite')

    try:
        max_order = WorksitesStatus.objects.filter(worksite_id=worksite_id, active=True).aggregate(max_order=Max('status__order'))['max_order']

        if max_order:
            next_status = Status.objects.get(order=max_order+1)
            updated_worksite_status = WorksitesStatus.objects.create(
                worksite_id=worksite_id, 
                status=next_status,
                active=True)
        return Response('tutto regolare') 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['POST'])
def undo_worksite_status(request):

    worksite_id = request.data.get('worksite')

    try:
        max_order = WorksitesStatus.objects.filter(worksite_id=worksite_id, active=True).aggregate(max_order=Max('status__order'))['max_order']

        if max_order:
            wk_status = WorksitesStatus.objects.filter(worksite_id=worksite_id, active=True, status__order=max_order).first()
            wk_status.active = False
            wk_status.save()

        return Response('tutto regolare') 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


    
    


@api_view(['PUT'])
def edit_order_collabworksite(request):
    profiles = request.data.get('profiles', [])

    for profile in profiles:
        
        collab = CollabWorksitesOrder.objects.get(id=profile['id'])
        collab.order = profile['order']
        collab.save()

    return Response('tutto regolare', status=status.HTTP_200_OK)
