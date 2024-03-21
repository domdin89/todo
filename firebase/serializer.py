from rest_framework import serializers
from firebase.models import LastVersion


class LastVersionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LastVersion
        fields = '__all__'