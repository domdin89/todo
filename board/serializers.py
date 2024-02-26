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
        queryset=Worksites.objects.all(), write_only=True, required=False, allow_null=True, source='worksites')
    apartment_id = serializers.PrimaryKeyRelatedField(
        queryset=Apartments.objects.all(), write_only=True, required=False, allow_null=True, source='apartment')
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), write_only=True, required=False, allow_null=True, source='profile')

    class Meta:
        model = BoardsRecipient
        fields = ['id', 'recipient_type', 'date', 'worksites_id', 'apartment_id', 'profile_id']

    def create(self, validated_data):
        # Validated data avrà i campi `worksites`, `apartment`, e `profile` direttamente grazie a `source`
        return BoardsRecipient.objects.create(**validated_data)

    def to_representation(self, instance):
        """
        Personalizza la rappresentazione in uscita per includere i dettagli completi
        delle entità relazionate, se presenti.
        """
        representation = super().to_representation(instance)
        representation['worksites'] = WorksiteStandardSerializer(instance.worksites).data if instance.worksites else None
        representation['apartment'] = ApartmentSerializer(instance.apartment).data if instance.apartment else None
        representation['profile'] = ProfileSerializer(instance.profile).data if instance.profile else None
        return representation

class BoardsSerializer(serializers.ModelSerializer):
    recipients = RecipientsSerializer(many=True)

    class Meta:
        model = Boards
        fields = ['id', 'image', 'title', 'body', 'author', 'date', 'date_update', 'type', 'recipients']

    def create(self, validated_data):
        # Estrai i dati dei destinatari (recipients) e rimuovili dai dati validati della board
        recipients_data = validated_data.pop('recipients', [])
        # Crea l'istanza della board
        board = Boards.objects.create(**validated_data)
        # Itera sui dati dei destinatari per creare le relative istanze di BoardsRecipient
        for recipient_data in recipients_data:
            # Crea ogni istanza di BoardsRecipient associata alla board corrente
            BoardsRecipient.objects.create(board=board, **recipient_data)
        return board
    
class BoardSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = "__all__"


class BoardRecipientSerializer(serializers.ModelSerializer):
    board = BoardSerializerNew(read_only=True)

    class Meta:
        model = BoardsRecipient
        fields = ['board']  # Usa una lista
