from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import filters

from worksites.filters import WorksitesFilter, WorksitesFilter2
from worksites.models import CollabWorksitesOrder, Worksites
from worksites.serializers import CollabWorksitesOrderSerializer, WorksiteSerializer
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView



class TecniciProfileListCreate(ListCreateAPIView):
    queryset = Profile.objects.filter(type='TECNICI')
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(type='TECNICI')
        
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class ProfileListCreateAPIView(ListCreateAPIView):
    queryset = Profile.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ['first_name', 'last_name', 'email']  # Aggiusta questi campi in base alle tue necessità di ricerca
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        type_param = self.request.GET.get('type', None)  # Use GET instead of query_params
        search_param = self.request.GET.get('search', None)
        order_param = self.request.GET.get('order', 'desc')
        order_by_field = self.request.GET.get('order_by', 'id')
        
        if order_param == 'desc':
            queryset = queryset.order_by('-' + order_by_field)
        else:
            queryset = queryset.order_by(order_by_field)

        if type_param is not None:
            queryset = queryset.filter(type=type_param)

        if search_param:
            queryset = queryset.filter(
                Q(first_name__icontains=search_param) | 
                Q(last_name__icontains=search_param) | 
                Q(email__icontains=search_param)
            )

        return queryset

class GenericListAPIView(APIView):
    model = None
    serializer_class = None
    filter_params = None
    default_page_size = 10
    default_order_by = 'id'
    search_param_name = 'search'
    filterset_class = None

    def get(self, request, format=None):
        try:
            params = {}
            for param in self.filter_params:
                params[param] = request.GET.get(param)

            page_param = request.GET.get('page', 1)
            page_size_param = request.GET.get('page_size', self.default_page_size)
            order_param = request.GET.get('order', 'asc')
            order_by_param = request.GET.get('order_by', self.default_order_by)

            queryset = self.model.objects.all()
            for key, value in params.items():
                if value:
                    queryset = queryset.filter(**{key: value})

            if order_param == 'asc':
                queryset = queryset.order_by(order_by_param)
            else:
                queryset = queryset.order_by('-' + order_by_param)

            search_param = request.GET.get(self.search_param_name)
            if search_param:
                filter_fields = self.get_search_fields()
                search_q = Q()
                for field in filter_fields:
                    search_q |= Q(**{field + '__icontains': search_param})
                queryset = queryset.filter(search_q)

            paginator = Paginator(queryset, page_size_param)
            
            try:
                queryset = paginator.page(page_param)
            except PageNotAnInteger:
                queryset = paginator.page(1)
            except EmptyPage:
                return Response({
                    'count': 0,
                    'page_size': page_size_param,
                    'current_page': page_param,
                    'results': []
                }, status=status.HTTP_200_OK)

            serializer = self.serializer_class(queryset, many=True)
            data = {
                'count': paginator.count,
                'page_size': page_size_param,
                'current_page': page_param,
                'results': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_search_fields(self):
        raise NotImplementedError("Subclasses must implement get_search_fields method")



class WorksiteListAPIView(GenericListAPIView):
    model = Worksites
    serializer_class = WorksiteSerializer
    filter_params = ['name', 'address']
    default_page_size = 20
    default_order_by = 'name'
    filterset_class = WorksitesFilter2

    def get_search_fields(self):
        return ['name', 'address']
    
class ProfileListAPIView(GenericListAPIView):
    model = Profile
    serializer_class = ProfileSerializer
    filter_params = ['role']
    default_page_size = 20
    default_order_by = 'last_name'


    def get_search_fields(self):
        return ['first_name', 'last_name', 'email', 'mobile_number', ]

class CollabWorksiteListAPIView(GenericListAPIView):
    model = CollabWorksitesOrder
    serializer_class = CollabWorksitesOrderSerializer
    filter_params = ['worksite']
    default_page_size = 20
    default_order_by = 'profile'

    def get_search_fields(self):
        return ['profile__first_name', 'profile__last_name', 'profile__email', 'profile__mobile_number']


class ProfileListCreateAPIView2(APIView):
    def get(self, request, format=None):
        profiles = Profile.objects.all()

        # Estrai i parametri dalla richiesta GET
        role_param = request.GET.get('role')
        page_param = request.GET.get('page', 1)
        page_size_param = request.GET.get('page_size', 10)
        order_param = request.GET.get('order', 'asc')
        order_by_param = request.GET.get('order_by', 'id')
        search_param = request.GET.get('search')

        # Filtra per ruolo se presente
        if role_param:
            profiles = profiles.filter(type=role_param)

        # Logica di ordinamento
        if order_param == 'asc':
            profiles = profiles.order_by(order_by_param)
        else:
            profiles = profiles.order_by('-' + order_by_param)

        # Logica di ricerca
        if search_param is not None:
            if search_param.strip():
                profiles = profiles.filter(
                    Q(first_name__icontains=search_param) |
                    Q(last_name__icontains=search_param) |
                    Q(email__icontains=search_param)
                )

        # Paginazione
        paginator = Paginator(profiles, page_size_param)
        page_number = page_param
        try:
            profiles = paginator.page(page_number)
        except PageNotAnInteger:
            profiles = paginator.page(1)
        except EmptyPage:
            profiles = paginator.page(paginator.num_pages)

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        profile_data = {
            'first_name': request.data.get('first_name', None),
            'last_name': request.data.get('last_name', None),
            'mobile_number': request.data.get('mobile_number', None),
            'email': request.data.get('email', None),
            'image': request.data.get('image', None)
        }


        profile_data = {key: value for key, value in profile_data.items() if value is not None}

        new_professionista = Profile.objects.create(**profile_data)

        serializer = ProfileSerializer(new_professionista)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profiles(request):
    # Estrai i parametri della query
    role_param = request.GET.get('role', None)
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    order = request.GET.get('order', 'asc')
    order_by = request.GET.get('order_by', 'first_name')
    search_param = request.GET.get('search', None)

    # Costruisci la queryset in base ai parametri
    profiles = Profile.objects.all()

    if role_param:
        profiles = profiles.filter(type=role_param)

    if search_param:
        profiles = profiles.filter(
            Q(first_name__icontains=search_param) |
            Q(last_name__icontains=search_param) |
            Q(email__icontains=search_param)
        )

    if order == 'desc':
        profiles = profiles.order_by('-' + order_by)
    else:
        profiles = profiles.order_by(order_by)

    # Applica la paginazione
    paginator = Paginator(profiles, page_size)
    try:
        profiles_page = paginator.page(page)
    except PageNotAnInteger:
        profiles_page = paginator.page(1)
    except EmptyPage:
        profiles_page = paginator.page(paginator.num_pages)

    serializer = ProfileSerializer(profiles_page, many=True, context={'request': request})
    return Response({
        'count': paginator.count,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'page_size': page_size,
        'results': serializer.data
    })

@api_view(['POST'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def profile_create(request):
    # Estrai i dati dalla richiesta
    post_data = {
        'first_name': request.data.get('first_name'),
        'last_name': request.data.get('last_name'),
        'mobile_number': request.data.get('mobile_number'),
        'email': request.data.get('email'),
        'image': request.FILES.get('image'),
        'type': 'TECNICI'
    }
    
    # Filtra i campi None
    post_data = {key: value for key, value in post_data.items() if value is not None}

    if not post_data:  # Se post_data è vuoto dopo la rimozione di valori None
        return Response({"detail": "Dati insufficienti per creare un profilo."}, status=status.HTTP_400_BAD_REQUEST)

    # Crea un nuovo profilo
    try:
        profile = Profile(**post_data)
        profile.save()
    except Exception as e:  # Cattura eventuali errori durante la creazione del profilo
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Profilo creato con successo."}, status=status.HTTP_201_CREATED)
    
api_view(['PUT'])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
def profile_edit(request):

    profile_id = request.data.get('profile_id', None)

    profile = Profile.objects.get(id=profile_id)

    post_data = {
    'first_name' : request.data.get('first_name', profile.first_name),
    'last_name' : request.data.get('last_name', profile.last_name),
    'mobile_number' : request.data.get('mobile_number', profile.mobile_number),
    'email' : request.data.get('email', profile.email),
    'image' : request.FILES.get('image', profile.image)
    }

    post_data = {key: value for key, value in post_data.items() if value is not None}

    # Aggiorna i campi del cantiere
    for key, value in post_data.items():
        setattr(profile, key, value)

    # Salva il cantiere
    profile.save()


    return Response("Cantiere aggiornato con successo", status=status.HTTP_200_OK)
