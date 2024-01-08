from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from accounts.models import Collaborators
from worksites.models import Worksites
from apartments.models import Apartments


class Boards(models.Model):  
    worksite = models.ForeignKey(
        Worksites, on_delete=models.CASCADE, blank=True, null=True, )
    apartment = models.ForeignKey(
        Apartments, on_delete=models.CASCADE, blank=True, null=True, )
    image = models.ImageField(
        upload_to='worksite_pic/', blank=True, null=True, )
    title = models.CharField(max_length=250, blank=True, null=True, )
    body = models.TextField()
    author = models.CharField(max_length=150, blank=True, null=True, )

    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def clean(self):
        # Controlla che almeno uno dei due campi non sia nullo
        if not (self.worksite or self.apartment):
            raise ValidationError("Deve essere impostato almeno uno tra cantiere o unità abitativa.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Boards, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} {self.date}"
    
class CollabWorksites(models.Model):  
    collaborator = models.ForeignKey(
        Collaborators, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='collabworksites_collaborators'
    )
    worksite = models.ForeignKey(
        Worksites, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='collabworksites_worksites'
    )
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.collaborator.first_name} {self.worksite}"
