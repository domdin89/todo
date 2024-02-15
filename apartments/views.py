from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ApartmentBaseSerializer, ClientApartmentsSerializer
from .models import Apartments, ClientApartments
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class ClientApartmentsListView(ListAPIView):
    queryset = ClientApartments.objects.all().select_related('apartment')
    serializer_class = ClientApartmentsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['profile__first_name', 'profile__last_name']  # Adjust based on search requirements

    def get_queryset(self):
        queryset = super().get_queryset()
        worksite = self.request.query_params.get('worksite')
        if worksite:
            queryset = queryset.filter(apartment__worksite__id=worksite)
        return queryset
    

class ApartmentListCreateAPIView(ListCreateAPIView):
    queryset = Apartments.objects.all()
    serializer_class = ApartmentBaseSerializer
    #permission_classes = [IsAuthenticated]
    
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['owner']
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
            queryset = super().get_queryset()
            order_param = self.request.GET.get('order', 'desc')
            order_by_field = self.request.GET.get('order_by', 'id')
            worksite = self.request.GET.get('worksite')
            
            if order_param == 'desc':
                queryset = queryset.order_by('-' + order_by_field)
            else:
                queryset = queryset.order_by(order_by_field)
            
            if worksite:
                queryset = queryset.filter(worksite=worksite)  # Filtra per worksite se presente
        
            return queryset
          
    def list(self, request, *args, **kwargs):
        worksite = request.query_params.get('worksite')
        if not worksite:
            return Response({"status": "fail", "message": "Attenzione, worksite obbligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        return super(ApartmentListCreateAPIView, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Handling multipart data including files
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)