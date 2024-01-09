from rest_framework import serializers
from .models import Boards
from worksites.serializers import WorksiteSerializer
from apartments.serializers import ApartmentSerializer


class BoardSerializer(serializers.ModelSerializer):
    worksite = WorksiteSerializer()
    apartment = ApartmentSerializer()

    class Meta:
        model = Boards
        fields = '__all__'