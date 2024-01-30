from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Apartments
from .serializers import WorksiteApartmentsSerializer

# Create your views here.
@login_required(login_url='accounts:login')
def apartments_api(request):
    apartments = Apartments.objects.all()
    serializer = WorksiteApartmentsSerializer(apartments, many=True)

    data = {
    'results': serializer.data,
    }

    return JsonResponse(data)