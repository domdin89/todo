from django.db import models
import os

from accounts.models import Profile
from apartments.models import Apartments
from worksites.models import Worksites
from falone.storage_backends import PrivateMediaStorage


class Directory(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subdirectories')
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE,  null=True, blank=True)
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE,  null=True, blank=True)
    apa = models.ForeignKey(Worksites, on_delete=models.CASCADE,  null=True, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE,  null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    class Meta:
        unique_together = (('name', 'worksite'), ('name', 'parent'))

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=10, blank=True, null=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='files/', storage=PrivateMediaStorage())
    size = models.PositiveBigIntegerField(blank=True, null=True)  # Dimensione del file in byte
    mime_type = models.CharField(max_length=50, blank=True, null=True)  # Tipo MIME del file
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Estrai l'estensione del file
        self.extension = os.path.splitext(self.file.name)[1][1:].lower()
        
        # Imposta la dimensione del file (assicurati che il file sia stato effettivamente caricato prima di fare questo)
        if self.file and not self.size:
            self.size = self.file.size
            
        # Qui potresti voler impostare il tipo MIME in base all'estensione o utilizzando un pacchetto esterno per determinarlo
        
        super(File, self).save(*args, **kwargs)