from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import filters
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class TecniciProfileListCreate(ListCreateAPIView):
    queryset = Profile.objects.filter(type='TECNICI')
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(type='TECNICI')


class ProfileListCreateAPIView(ListCreateAPIView):
    queryset = Profile.objects.all()
    #permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']  # Aggiusta questi campi in base alle tue necessità di ricerca

    def get_queryset(self):
        queryset = super().get_queryset()
        type_param = self.request.query_params.get('type', None)
        search_param = self.request.query_params.get('search', None)
        order_param = self.request.query_params.get('order', 'desc')
        order_by_field = self.request.query_params.get('order_by', 'id')  # Prendi il campo da 'order_by', default a 'id'
        
        # Applica direttamente l'ordinamento
        if order_param == 'desc':
            queryset = queryset.order_by('-' + order_by_field)  # Ordinamento discendente
        else:
            queryset = queryset.order_by(order_by_field)  # Ordinamento ascendente

        if type_param is not None:
            queryset = queryset.filter(type=type_param)

        if search_param:
            queryset = queryset.filter(
                Q(first_name__icontains=search_param) | 
                Q(last_name__icontains=search_param) | 
                Q(email__icontains=search_param)
            )

        return queryset
