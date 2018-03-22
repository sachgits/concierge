from django.db.models.signals import post_save
from django.dispatch import receiver

from saml.models import IdentityProvider

@receiver(post_save, sender=IdentityProvider)
def renew_x509certs(sender, instance, created, **kwargs):
    if created:
        instance.get_idp_x509certs()
