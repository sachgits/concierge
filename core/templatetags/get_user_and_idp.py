from django import template
from core.models import User
from saml.models import IdpEmailDomains

register = template.Library()

@register.simple_tag
def get_user_and_idp(email):
    idp_shortname = None
    user = None

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        pass

    try:
        email_domain = email.split('@')[1]
        try:
            idp_shortname = IdpEmailDomains.objects.get(email_domain=email_domain).identityprovider
        except IdpEmailDomains.DoesNotExist:
            pass
    except IndexError:
        pass

    return {
        "user": user,
        "idp": idp_shortname 
    }
