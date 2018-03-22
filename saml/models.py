from django.db import models
from django.utils.text import slugify
from django.contrib import admin
from django.conf import settings
from django.core import signing
from core.models import User
from urllib.request import urlopen
from lxml import etree

class IdentityProvider(models.Model):
    shortname = models.SlugField(unique=True)
    displayname = models.CharField(max_length=100, null=False)
    entityId = models.URLField(max_length=256, null=False)
    ssoId = models.URLField(max_length=256, null=False)
    sloId = models.URLField(max_length=256, blank=True)
    x509cert1 = models.TextField(blank=True)
    x509cert2 = models.TextField(null=True, blank=True)

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
            "x509certMulti": {
	            "signing": [self.x509cert1, self.x509cert2] 
            }     
        }

    def get_idp_x509certs(self):
        idp_metadata = etree.fromstring(urlopen(self.entityId).read())
        namespace = idp_metadata.nsmap
        x509certs = []
        signing_x509certs = idp_metadata.findall("./md:IDPSSODescriptor/md:KeyDescriptor[@use='signing']/ds:KeyInfo/ds:X509Data", namespace)
        if not signing_x509certs:
            #when default namespace is used for root elements
            signing_x509certs = idp_metadata.findall("./IDPSSODescriptor/KeyDescriptor[@use='signing']/ds:KeyInfo/ds:X509Data", namespace)
            
        for x509cert in signing_x509certs:
            x509certs.append(x509cert.findtext("ds:X509Certificate", namespaces=namespace))
        need_save = False
        try:
            self.x509cert1 = x509certs[0]
            need_save = True
            try:
                self.x509cert2 = x509cert[1]
            except IndexError: 
                pass
        except IndexError:
            pass    
        
        if need_save:
            self.save()
                

class ExternalIds(models.Model):
    identityproviderid = models.ForeignKey('IdentityProvider', on_delete=models.CASCADE, db_index=True)
    externalid = models.CharField(max_length=100, db_index=True, unique=True)
    userid = models.ForeignKey('core.User', on_delete=models.CASCADE, db_index=True)


admin.site.register(IdentityProvider)