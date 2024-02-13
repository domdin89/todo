from rest_framework import serializers
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from apartments.models import Apartments
from apartments.serializers import ApartmentSerializer
from worksites.models import Worksites

from worksites.serializers import WorksiteStandardSerializer
from .models import Boards, BoardsRecipient

class RecipientsSerializer(serializers.ModelSerializer):
    worksite_id = serializers.PrimaryKeyRelatedField(
        queryset=Worksites.objects.all(), source='worksites', write_only=True, required=False)
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartments.objects.all(), source='apartment', write_only=True, required=False)
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), source='profile', write_only=True, required=False)

    class Meta:
        model = BoardsRecipient
        exclude = ['board']

class BoardsSerializer(serializers.ModelSerializer):
    recipients = RecipientsSerializer(many=True)

    class Meta:
        model = Boards
        fields = ['id', 'image', 'title', 'body', 'author', 'date', 'date_update', 'type', 'recipients']

    def create(self, validated_data):
        recipients_data = validated_data.pop('recipients', [])
        board = Boards.objects.create(**validated_data)
        for recipient_data in recipients_data:
            # Estrai i dati dei campi nidificati dopo la popolazione della chiave esterna 'board'
            recipient_data = recipient_data.get('recipients') if 'recipients' in recipient_data else recipient_data
            BoardsRecipient.objects.create(board=board, **recipient_data)
        return board