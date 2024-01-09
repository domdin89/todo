from rest_framework import serializers
from .models import Worksites


class WorksiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worksites
        fields = '__all__'