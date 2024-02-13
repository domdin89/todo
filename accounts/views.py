from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import filters
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

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