from django.db.models.signals import post_save
from django.dispatch import receiver
from apartments.models import WBS, WBSWorksite
from file_manager.models import Directory
from .models import Status, Worksites, WorksitesStatus

@receiver(post_save, sender=Worksites)
def initWorksiteStatus(sender, instance, created, **kwargs):
    if created:  # Esegui solo se l'istanza è stata appena creata
        try:
            initial_status = Status.objects.order_by('order').first()
            if initial_status:  # Assicurati che ci sia almeno uno status
                WorksitesStatus.objects.create(
                    status=initial_status,
                    worksite=instance  # Usa l'istanza passata dalla funzione
                )
        except Status.DoesNotExist:
            # Gestisci il caso in cui non ci siano oggetti Status nel database
            pass

@receiver(post_save, sender=Worksites)
def initWorksiteWBS(sender, instance, created, **kwargs):
    if created:  # Esegui solo se l'istanza è stata appena creata
        try:
            # Assicurati di avere una directory principale per questo cantiere
            main_directory, created = Directory.objects.get_or_create(
                name=instance.name,
                worksite=instance,
                type=Directory.DirectoryType.WORKSITE
            )

            if WBS.objects.exists():  # Verifica se ci sono WBS nel database
                wbs_items = WBS.objects.all()
                wbs_worksite_objects = [
                    WBSWorksite(wbs=wbs_item, worksite=instance) for wbs_item in wbs_items
                ]
                wbs_worksites = WBSWorksite.objects.bulk_create(wbs_worksite_objects)
            
                for wbs_worksite in wbs_worksites:
                    Directory.objects.create(
                        name=wbs_worksite.wbs.nome,  # Usa il nome del WBS come nome della Directory
                        parent=main_directory,  # Imposta la directory principale come parent
                        worksite=instance,
                        type=Directory.DirectoryType.WBS
                    )
        except Exception as e:
            print(f"Error during initWorksiteWBS signal: {e}")
            pass

@receiver(post_save, sender=WBSWorksite)
def initWBSWorksite(sender, instance, created, **kwargs):
    if created:  # Esegui solo se l'istanza è stata appena creata
        try:           
            main_dir, created = Directory.objects.get_or_create(
                worksite=instance.worksite,
                type=Directory.DirectoryType.WORKSITE
            )
            
            Directory.objects.create(
                name=instance.wbs.nome,  # Usa il nome del WBS come nome della Directory
                parent=main_dir,  # Imposta la directory principale come parent
                worksite=instance.worksite,
                type=Directory.DirectoryType.WBS
            )
        except Exception as e:
            print(f"Error during initWorksiteWBS signal: {e}")
            pass