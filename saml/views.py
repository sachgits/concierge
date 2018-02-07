from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from django.template import RequestContext
from saml.models import IdentityProvider, ExternalIds
from core.models import User
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login

def init_saml_auth(req, idp_shortname=None):
    try:
        idp = IdentityProvider.objects.get(shortname=idp_shortname)
    except IdentityProvider.DoesNotExist:
        idp = None
    
    if idp:
        configuration = {
            "strict": True,
            "debug": settings.DEBUG,
            "sp": settings.SAML2_SP,
            "idp": idp.get_saml_configuration()
        }

        auth = OneLogin_Saml2_Auth(req, configuration)
        return auth

    return None

def prepare_django_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'get_data': request.GET.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.POST.copy()
    }
    return result

@csrf_exempt
def saml(request):
    req = prepare_django_request(request)
    if request.session.get('slo'):
        request.session.pop('slo')
        req['get_data']['slo'] = 'slo'
        
    if 'idp' in req['get_data']:
        request.session['idp'] = req['get_data']['idp']
    idp_shortname = request.session.get('idp') or None

    if not idp_shortname:
        return redirect(settings.LOGIN_REDIRECT_URL)        

    auth = init_saml_auth(req, idp_shortname=idp_shortname)

    attributes = []
    name_id = None
    session_index = None

    if 'sso' in req['get_data']:
        return HttpResponseRedirect(auth.login())

    elif 'acs' in req['get_data']:
        auth.process_response()
        errors = auth.get_errors()

        if not errors:
            attributes = auth.get_attributes()
            name_id = auth.get_nameid()
            session_index = auth.get_session_index()
            
            request.session['samlUserdata'] = attributes
            request.session['samlNameId'] = name_id
            request.session['samlSessionIndex'] = session_index

            email = attributes.get('email')[0]
            extid = ExternalIds.check_externalid(shortname=idp_shortname, externalid=email)
            user = User.objects.get(pk=extid.userid.pk)
            auth_login(request, user)
            request.session['samlLogin'] = True

        return redirect(settings.LOGIN_REDIRECT_URL)

    elif 'slo' in req['get_data']:
        return HttpResponseRedirect(auth.logout(
            return_to=settings.LOGOUT_REDIRECT_URL,
            name_id=request.session.get('samlNameId'),
            session_index=request.session.get('samlSessionIndex')
        ))

    elif 'sls' in req['get_data']:
        # do nothing, because a user never logges in at our place
        return redirect(settings.LOGOUT_REDIRECT_URL)

    return render(request, 'saml.html', {
        'is_authenticated': auth.is_authenticated(),
        'name_id': name_id,
        'attributes': attributes,
        'session_index': session_index
    })

def attrs(request):
    paint_logout = False
    attributes = False

    if 'samlUserdata' in request.session:
        paint_logout = True
        if len(request.session['samlUserdata']) > 0:
            attributes = request.session['samlUserdata'].items()

    return render(request, 'saml_attrs.html', 
                    context=RequestContext(request, {
                        'paint_logout': paint_logout, 
                        'attributes': attributes
                        }).flatten())


def metadata(request):
    # req = prepare_django_request(request)
    # auth = init_saml_auth(req)
    # saml_settings = auth.get_settings()
    saml_settings = OneLogin_Saml2_Settings(settings=None, custom_base_path=settings.SAML_FOLDER, sp_validation_only=True)
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type='text/xml')
    else:
        resp = HttpResponseServerError(content=', '.join(errors))
    return resp
