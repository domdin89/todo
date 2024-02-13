from rest_framework import serializers
from accounts.serializers import ProfileSerializer
from apartments.serializers import ApartmentSerializer

from worksites.serializers import WorksiteStandardSerializer
from .models import Boards, BoardsRecipient

class RecipientsSerializer(serializers.ModelSerializer):
    worksites = WorksiteStandardSerializer()
    apartment = ApartmentSerializer()
    profile = ProfileSerializer()

    class Meta:
        model = BoardsRecipient
        fields = '__all__'

class BoardsSerializer(serializers.ModelSerializer):
    recipients = RecipientsSerializer(many=True, read_only=True)

    class Meta:
        model = Boards
        fields = ['id', 'image', 'title', 'body', 'author', 'date', 'date_update', 'recipients', 'type']
       