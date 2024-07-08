from django.db.models.signals import post_save
from django.dispatch import receiver
from apartments.models import WBS, Room, WBSRoom, WBSWorksite
from file_manager.models import Directory

@receiver(post_save, sender=Room)
def initRoomWBS(sender, instance, created, **kwargs):
    if created:  # Esegui solo se l'istanza è stata appena creata
        try:
            # Assicurati di avere una directory principale per questo apartment
            parent_directory = Directory.objects.filter(
                apartment=instance.apartment,
                type=Directory.DirectoryType.APARTMENT
            ).first()

            if not parent_directory:
                print(f"Parent directory for apartment {instance.apartment} not found.")
                return
            
            # Crea una directory per la stanza
            room_directory = Directory.objects.create(
                name=instance.nome,
                parent=parent_directory,
                room=instance,
                type=Directory.DirectoryType.ROOM
            )

            if WBS.objects.exists():
                wbs_items = WBS.objects.filter(wbsworksite__is_active=True, wbsworksite__worksite=instance.apartment.worksite)
                wbs_room_objects = [
                    WBSRoom(wbs=wbs_item, room=instance) for wbs_item in wbs_items
                ]
                WBSRoom.objects.bulk_create(wbs_room_objects)
            
                for wbs_item in wbs_items:
                    Directory.objects.create(
                        name=wbs_item.nome,
                        parent=room_directory,
                        room=instance,
                        type=Directory.DirectoryType.WBS
                    )
        except Exception as e:
            print(f"Error during initRoomWBS signal: {e}")
            pass