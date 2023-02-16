from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Customer

User = get_user_model()


@receiver(post_save, sender=User)
def create_customer_instance(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
