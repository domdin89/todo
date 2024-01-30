from rest_framework import serializers
from .models import Worksites
from accounts.serializers import ProfileSerialAll


class WorksiteSerializer(serializers.ModelSerializer):
    user = ProfileSerialAll()

    class Meta:
        model = Worksites
        fields = '__all__'