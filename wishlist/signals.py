from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Wishlist

@receiver(post_save, sender=User)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)