from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer

class TecniciProfileListCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.filter(type='TECNICI')
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(type='TECNICI')
