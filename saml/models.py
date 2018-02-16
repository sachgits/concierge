from django.db import models
from django.utils.text import slugify
from django.contrib import admin
from django.conf import settings
from django.core import signing
from core.models import User

class IdentityProvider(models.Model):
    shortname = models.SlugField(unique=True)
    displayname = models.CharField(max_length=100, null=False)
    entityId = models.URLField(max_length=256, null=False)
    ssoId = models.URLField(max_length=256, null=False)
    sloId = models.URLField(max_length=256, null=False)
    x509cert = models.CharField(max_length=8192, null=False)

    def __str__(self):
        return self.shortname

    def get_saml_configuration(self):
        return {
            "entityId": self.entityId,
            "singleSignOnService": {
                "url": self.ssoId,
                "binding": settings.SAML_IDP_BINDING
            },
            "singleLogoutService": {
                "url": self.sloId,
                "binding": settings.SAML_IDP_BINDING
            },
            "x509cert": self.x509cert
        }


class ExternalIds(models.Model):
    identityproviderid = models.ForeignKey('IdentityProvider', on_delete=models.CASCADE, db_index=True)
    externalid = models.CharField(max_length=100, db_index=True, unique=True)
    userid = models.ForeignKey('core.User', on_delete=models.CASCADE, db_index=True)


admin.site.register(IdentityProvider)