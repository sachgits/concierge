from django.contrib import admin
from saml.models import IdentityProvider, IdpEmailDomains

# Register your models here.


class IdentityProviderAdmin(admin.ModelAdmin):
    fields = ['shortname' ,
              'displayname' ,
              'entityId' ,
              'perform_slo' 
            ]

admin.site.register(IdentityProvider, IdentityProviderAdmin)


class IdpEmailDomainsAdmin(admin.ModelAdmin):
    list_display = ('email_domain', 'identityprovider')

admin.site.register(IdpEmailDomains, IdpEmailDomainsAdmin)



