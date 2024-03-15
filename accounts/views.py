from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import filters
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes, permission_classes
from rest_framework.parsers import MultiPartParser
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



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
