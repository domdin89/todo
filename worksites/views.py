from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from accounts.serializers import ProfileSerializer

from worksites.filters import WorksitesFilter
from .models import CollabWorksites, Worksites
from .serializers import CollaborationSerializer, WorksiteProfileSerializer, WorksiteSerializer
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

from .models import CollabWorksites, Profile, Worksites
from .serializers import CollaborationSerializer

from accounts.models import Profile

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class WorksiteListView(ListCreateAPIView):
    queryset = Worksites.objects.all()
    serializer_class = WorksiteSerializer
    permission_classes = [IsAuthenticated]
    
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filterset_class = WorksitesFilter
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        status = self.request.query_params.get('status', None)
        
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
    
    def post(self, request, *args, **kwargs):
        # Handling multipart data including files
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
class WorksiteDetail(RetrieveUpdateAPIView):
    queryset = Worksites.objects.all()
    serializer_class = WorksiteSerializer
    lookup_field = 'pk'



class CollaboratorListView(ListCreateAPIView):
    queryset = CollabWorksites.objects.all()
    serializer_class = CollaborationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['profile__first_name', 'profile__last_name', 'worksite__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        worksite = self.request.query_params.get('worksite', None)
        order_param = self.request.query_params.get('order', 'desc')
        order_by_field = self.request.query_params.get('order_by', 'id')  # Prendi il campo da 'order_by', default a 'id'
        
        # Applica direttamente l'ordinamento
        if order_param == 'desc':
            queryset = queryset.order_by('-' + order_by_field)  # Ordinamento discendente
        else:
            queryset = queryset.order_by(order_by_field)  # Ordinamento ascendente
        if worksite:
            return queryset.filter(worksite=worksite)
        return queryset


    def post(self, request, *args, **kwargs):
        profile_id = request.data.get('profile')
        worksite_id = request.data.get('worksite')
        role = request.data.get('role')
        order = request.data.get('order')

        profile = get_object_or_404(Profile, id=profile_id)
        worksite = get_object_or_404(Worksites, id=worksite_id)

        collab_worksite = CollabWorksites.objects.create(
            profile=profile,
            worksite=worksite,
            role=role,
            order=order
        )

        serializer = self.get_serializer(collab_worksite)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
    

class CollaboratorUpdateView(RetrieveUpdateAPIView):
    queryset = CollabWorksites.objects.all()
    serializer_class = CollaborationSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class WorksiteProfileListView(ListCreateAPIView):
    serializer_class = WorksiteProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['profile__first_name', 'profile__last_name', 'worksite__name']

    def get_queryset(self):
        queryset = CollabWorksites.objects.all()
        worksite_id = self.request.query_params.get('worksite')
        role = self.request.query_params.get('role')
        order_param = self.request.query_params.get('order', 'desc')
        order_by_field = self.request.query_params.get('order_by', 'id')  # Prendi il campo da 'order_by', default a 'id'
        
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


class TechnicianNotInWorksiteView(ListAPIView):
    #permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer  # Usa il serializer appropriato per Profile

    def get_queryset(self):
        # Seleziona tutti i profili di tipo 'TECNICI'
        queryset = Profile.objects.filter(type='TECNICI')
        
        # Recupera il parametro 'worksite' dalla richiesta
        worksite_id = self.request.query_params.get('worksite')
        
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