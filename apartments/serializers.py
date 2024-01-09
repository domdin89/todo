from rest_framework import serializers
from .models import Apartments

class ApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Apartments
        fields = '__all__'