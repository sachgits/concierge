from django.contrib import admin
from core.models import User, PleioPartnerSite, PleioLegalText
from saml.models import IdentityProvider

# Register your models here.
admin.site.register(User)
admin.site.register(PleioPartnerSite)
admin.site.register(PleioLegalText)

#admin.site.register(IdentityProvider)
class IdentityProviderAdmin(admin.ModelAdmin):
    fields = ['shortname' ,
              'displayname' ,
              'entityId' ,
              'perform_slo' 
            ]

admin.site.register(IdentityProvider, IdentityProviderAdmin)