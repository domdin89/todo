from rest_framework import serializers

from apartments.models import ApartmentSub, Apartments
from .models import FoglioParticella, Worksites, CollabWorksites, Contractor, Financier, Categories, WorksitesCategories, WorksitesFoglioParticella, WorksitesProfile
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class CollabWorksitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollabWorksites
        fields = "__all__"

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = "__all__"

class FinancierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financier
        fields = "__all__"

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"

class CollaborationSerializerEdit(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    class Meta:
        model = CollabWorksites
        fields = ['id', 'profile', 'worksite', 'role', 'order']

class CollaborationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CollabWorksites
        fields = ['id', 'profile', 'worksite', 'role', 'order']
class WorksiteStandardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worksites
        fields = '__all__'

class WorksiteCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorksitesCategories
        fields = ["id", "category", "worksite"]

class ApartmentSubSerializer(serializers.ModelSerializer):

    class Meta:
        model= ApartmentSub
        fields='__all__'

class ApartmentSerializer(serializers.ModelSerializer):
    sub = ApartmentSubSerializer(read_only=True, many=True)
    class Meta:
        model= Apartments
        fields='__all__'

class WorksiteProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    
    class Meta:
        model = CollabWorksites
        fields = ['profile', 'worksite', 'role', 'order']


class WorksiteUserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    apartments = serializers.SerializerMethodField()

    def get_apartments(self, obj):
        worksite_id = obj.worksite_id
        # Ottieni tutte le sottounità dell'appartamento associate al worksite
        apartment_subs = ApartmentSub.objects.filter(apartment__worksite=worksite_id)
        # Serializza i dati delle sottounità dell'appartamento
        serializer = ApartmentSubSerializer(instance=apartment_subs, many=True)
        return serializer.data
    
    class Meta:
        model = WorksitesProfile
        fields = ['profile', 'worksite', 'apartments']



class FoglioParticellaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoglioParticella
        fields = '__all__'

class WorksiteFoglioParticellaSerializer(serializers.ModelSerializer):
    foglio_particella = FoglioParticellaSerializer()

    class Meta:
        model = WorksitesFoglioParticella
        fields = '__all__'

class WorksiteSerializer(serializers.ModelSerializer):
    financier = FinancierSerializer(read_only=True)
    contractor = ContractorSerializer(read_only=True)
    categories = WorksiteCategoriesSerializer(many=True, read_only=True)  # Assumendo una relazione ManyToMany con Worksites
    collaborations = WorksiteProfileSerializer(many=True, read_only=True)
    foglio_particelle = WorksiteFoglioParticellaSerializer(many=True, read_only=True)

    class Meta:
        model = Worksites
        fields = ['id', 'image', 'name', 'address', 'lat', 'lon', 'is_visible', 'net_worth', 'percentage_worth', 'financier', 'contractor', 'link', 'date', 
                  'date_update', 
                  'collaborations', 'categories', 'status', 'codice_commessa', 'codice_CIG', 'codice_CUP', 'date_start', 'date_end', 'foglio_particelle']

