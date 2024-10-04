from django.db.models.signals import post_migrate
from django.dispatch import receiver
from ..models import IconPerfil
import os
from django.core.files import File
from django.conf import settings

@receiver(post_migrate)
def create_iconperfil(sender, **kwargs):
    if sender.name == 'apps.authentication':
        icon_dir = os.path.join(settings.BASE_DIR, 'apps/authentication/icons/')
        if os.path.exists(icon_dir):
            for icon_file in os.listdir(icon_dir):
                if icon_file.endswith(('png', 'jpg', 'jpeg')):
                    icon_path = os.path.join(icon_dir, icon_file)

                    with open(icon_path, 'rb') as f:
                        icon = IconPerfil()
                        icon.image.save(icon_file, File(f))
                        icon.name = os.path.splitext(icon_file[0])
                        icon.save()

