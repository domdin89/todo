from rest_framework import serializers
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from apartments.models import Apartments
from apartments.serializers import ApartmentSerializer
from worksites.models import Worksites

from worksites.serializers import WorksiteStandardSerializer
from .models import Boards, BoardsRecipient

class RecipientsSerializer(serializers.ModelSerializer):
    worksites_id = serializers.PrimaryKeyRelatedField(
        queryset=Worksites.objects.all(), write_only=True, source='worksites', required=False)
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartments.objects.all(), write_only=True, source='apartment', required=False)
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), write_only=True, source='profile', required=False)

    worksites = WorksiteStandardSerializer(read_only=True, required=False, allow_null=True)
    apartment = ApartmentSerializer(read_only=True, required=False, allow_null=True)
    profile = ProfileSerializer(read_only=True, required=False, allow_null=True)

    class Meta:
        model = BoardsRecipient
        fields = ['id', 'worksites_id', 'apartment_id', 'profile_id', 'worksites', 'apartment', 'profile']

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