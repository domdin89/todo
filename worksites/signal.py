from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Status, Worksites, WorksitesStatus

@receiver(post_save, sender=Worksites)
def generate_invoice_order(sender, instance, **kwargs):

    worksite = Worksites.objects.get(id=instance.id)

    status = WorksitesStatus.objects.filter(is_active=True)

    if not status:
        initial_status = Status.objects.order_by('order').first()

        wk_status = WorksitesStatus.objects.create(
            status=initial_status,
            worksite=worksite
        )