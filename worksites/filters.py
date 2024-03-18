import django_filters
from .models import Worksites, Categories

class WorksitesFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Categories.objects.all(),
        field_name='categories__category',  # Usa il related_name e specifica che stiamo filtrando attraverso la FK category
        to_field_name='id',
        label="Categoria"
    )

    class Meta:
        model = Worksites
        fields = []
    



class WorksitesFilter2(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Categories.objects.all(),
        field_name='categories__category',  # Usa il related_name e specifica che stiamo filtrando attraverso la FK category
        to_field_name='id',
        label="Categoria"
    )

    class Meta:
        model = Worksites
        fields = []

    def get_filter_params(self):
        return ['category']  # Aggiungi qui eventuali altri parametri di filtro