from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Boards
from .serializers import BoardsSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # Allows clients to dynamically adjust page size

class BoardsListView(ListAPIView):
    queryset = Boards.objects.all()
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'body', 'author']  # Aggiusta secondo le necessità
    filterset_fields = ['type']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    

# class WorksiteListView(ListCreateAPIView):
#     queryset = Worksites.objects.all()
#     serializer_class = WorksiteSerializer
#     #permission_classes = [IsAuthenticated]
    
#     pagination_class = CustomPagination
#     filter_backends = [SearchFilter, DjangoFilterBackend]
#     search_fields = ['name', 'address']
#     filterset_class = WorksitesFilter
#     parser_classes = (MultiPartParser, FormParser)

#     def get_queryset(self):
#         queryset = super().get_queryset().order_by('-id')
#         status = self.request.query_params.get('status', None)
        
#         if status is not None:
#             try:
#                 status = int(status)
#             except ValueError:
#                 return queryset.none()  # Return an empty queryset if status is invalid
            
#             if status == 0:
#                 return queryset
#             elif status == 1:
#                 return queryset.filter(is_open=True)
#             elif status == 2:
#                 return queryset.filter(is_open=False)

#         return queryset
    
#     def post(self, request, *args, **kwargs):
#         # Handling multipart data including files
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)