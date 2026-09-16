import os, logging
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import MenuImage, RoomImage, PackageImage   # tambah model lain di sini

logger = logging.getLogger(__name__)

def _delete_file(path: str):
    """Utility kecil untuk benar-benar menghapus file di filesystem."""
    if path and os.path.isfile(path):
        os.remove(path)
        logger.info(f"Deleted file: {path}")
    else:
        logger.warning(f"File not found or empty: {path}")

# ------------- 1) Hapus file bila record di-DELETE -------------
@receiver(post_delete, sender=MenuImage)
@receiver(post_delete, sender=RoomImage)
@receiver(post_delete, sender=PackageImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        _delete_file(instance.image.path)

# ------------- 2) Hapus file lama bila field image di-update / dikosongkan -------------
@receiver(pre_save, sender=MenuImage)
@receiver(pre_save, sender=RoomImage)
@receiver(pre_save, sender=PackageImage)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:                               # objek baru → tidak ada file lama
        return
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return

    new_file = instance.image
    # kondisi 1: user menghapus (new_file is None/False)
    # kondisi 2: user mengganti file (path lama ≠ path baru)
    if not new_file or old_file != new_file:
        _delete_file(old_file.path)