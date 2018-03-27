from django.contrib import admin
from saml.models import IdentityProvider, IdpEmailDomains

# Register your models here.

admin.site.register(IdpEmailDomains)

class IdentityProviderAdmin(admin.ModelAdmin):
    fields = ['shortname' ,
              'displayname' ,
              'entityId' ,
              'perform_slo' 
            ]

admin.site.register(IdentityProvider, IdentityProviderAdmin)



