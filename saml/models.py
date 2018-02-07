from django.db import models
from django.utils.text import slugify
from django.contrib import admin
from django.conf import settings
from core.models import User

class IdentityProvider(models.Model):
    shortname = models.SlugField(unique=True)
    displayname = models.CharField(max_length=100, null=False)
    entityId = models.URLField(max_length=256, null=False)
    ssoId = models.URLField(max_length=256, null=False)
    sloId = models.URLField(max_length=256, null=False)
    x509cert = models.CharField(max_length=8192, null=False)

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
    userid = models.ForeignKey('core.User')

    def check_externalid(**kwargs):
        shortname=kwargs.get('shortname') 
        externalid=kwargs.get('externalid')
        try:
            idp = IdentityProvider.objects.get(shortname=shortname)
        except IdentityProvider.DoesNotExist:
            return None

        try:
            user = User.objects.get(email=externalid)
        except User.DoesNotExist:
            user = User.objects.create_user(
                email=externalid,
                name=externalid,
                password="self.generate_password",
                accepted_terms=True,
                receives_newsletter=False
            )
            user.is_active=True
            user.save()

        try:
            extid = ExternalIds.objects.get(identityproviderid=idp, externalid=externalid)
        except ExternalIds.DoesNotExist:
            extid= ExternalIds.objects.create(
                identityproviderid=idp,
                externalid=externalid,
                userid=user
            )

        return extid


admin.site.register(IdentityProvider)