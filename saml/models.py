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
    perform_slo = models.BooleanField(default=True)
    ssoId = models.URLField(max_length=256, blank=True)
    sloId = models.URLField(max_length=256, blank=True)
    signing_x509cert1 = models.TextField(blank=True)
    signing_x509cert2 = models.TextField(blank=True)
    encryption_x509cert1 = models.TextField(blank=True)
    encryption_x509cert2 = models.TextField(blank=True)

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
	            "signing": [self.signing_x509cert1, self.signing_x509cert2], 
	            "encryption": [self.encryption_x509cert1, self.encryption_x509cert2], 
            }     
        }

    def get_idp_metadata(self):
        idp_metadata = etree.fromstring(urlopen(self.entityId).read())
        namespace = idp_metadata.nsmap
        if namespace.get('ds'):
            ds = 'ds:'
        else:
             ds = ''
        if namespace.get('md'):
            md = 'md:'
        else:
             md = ''

        sso = idp_metadata.findall("./"+md+"IDPSSODescriptor/"+md+"SingleSignOnService[@Binding='"+settings.SAML_IDP_BINDING+"']", namespace)
        self.ssoId = sso[0].attrib.get('Location', None)
        print('ssoid: ', self.ssoId)

        slo = idp_metadata.findall("./"+md+"IDPSSODescriptor/"+md+"SingleLogoutService[@Binding='"+settings.SAML_IDP_BINDING+"']", namespace)
        self.sloId = slo[0].attrib.get('Location', None)
        print('sloid: ', self.sloId)

        x509certs = []
        signing_x509certs = idp_metadata.findall("./"+md+"IDPSSODescriptor/"+md+"KeyDescriptor[@use='signing']/"+ds+"KeyInfo/ds:X509Data", namespace)
            
        for x509cert in signing_x509certs:
            x509certs.append(x509cert.findtext(ds+"X509Certificate", namespaces=namespace))
        
        try:
            self.signing_x509cert1 = x509certs[0]
            try:
                self.signing_x509cert2 = x509cert[1]
            except IndexError: 
                pass
        except IndexError:
            pass    

        x509certs = []
        encryption_x509certs = idp_metadata.findall("./"+md+"IDPSSODescriptor/"+md+"KeyDescriptor[@use='encryption']/"+ds+"KeyInfo/ds:X509Data", namespace)
            
        for x509cert in encryption_x509certs:
            x509certs.append(x509cert.findtext(ds+"X509Certificate", namespaces=namespace))
        
        try:
            self.encryption_x509cert1 = x509certs[0]
            try:
                self.encryption_x509cert2 = x509cert[1]
            except IndexError: 
                pass
        except IndexError:
            pass    
        
        self.save()
                

class ExternalIds(models.Model):
    identityproviderid = models.ForeignKey('IdentityProvider', on_delete=models.CASCADE, db_index=True)
    externalid = models.CharField(max_length=100, db_index=True, unique=True)
    userid = models.ForeignKey('core.User', on_delete=models.CASCADE, db_index=True)
