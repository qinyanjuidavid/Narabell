from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from modules.accounts.models import Administrator, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == "Administrator" or instance.is_admin or instance.is_staff:
            Administrator.objects.create(user=instance)
