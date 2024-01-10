from rest_framework import serializers
from .models import Apartments
from worksites.serializers import WorksiteSerializer

class ApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Apartments
        fields = '__all__'




class WorksiteApartmentsSerializer(serializers.ModelSerializer):
    worksite = WorksiteSerializer()

    class Meta:
        model = Apartments
        fields = '__all__'