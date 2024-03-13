from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import filters
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes
from rest_framework.parsers import MultiPartParser



class TecniciProfileListCreate(ListCreateAPIView):
    queryset = Profile.objects.filter(type='TECNICI')
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(type='TECNICI')
        
class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class ProfileListCreateAPIView(ListCreateAPIView):
    queryset = Profile.objects.filter(is_active=True)
    #permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = CustomPagination
    search_fields = ['first_name', 'last_name', 'email']  # Aggiusta questi campi in base alle tue necessità di ricerca

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
    
api_view(['PUT'])
@parser_classes([MultiPartParser])
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
