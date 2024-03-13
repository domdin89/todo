from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Status, Worksites, WorksitesStatus

@receiver(post_save, sender=Worksites)
def generate_invoice_order(sender, instance, created, **kwargs):

    if created:  # Esegui solo se l'istanza è stata appena creata
        try:
            initial_status = Status.objects.order_by('order').first()
        except Status.DoesNotExist:
            # Gestisci il caso in cui non ci siano oggetti Status nel database
            return
        
        WorksitesStatus.objects.create(
            status=initial_status,
            worksite=instance  # Usa l'istanza passata dalla funzione
        )