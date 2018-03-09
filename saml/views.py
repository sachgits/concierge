from django.shortcuts import render, redirect
from django.conf import settings
from django.core import signing
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib import messages
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from django.template import RequestContext
from django.utils.translation import gettext, gettext_lazy as _
from saml.models import IdentityProvider, ExternalIds
from saml.forms import SetPasswordForm, ShowConnectionsForm
from core.models import User, EventLog
from core.class_views import PleioLoginView
from core.forms import PleioAuthenticationForm
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login
import requests
from core.forms import UserProfileForm

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
    http_host = settings.EXTERNAL_HOST
    if '://' in http_host:
        http_host = http_host.split('://')[1]
    result = {
        'https': 'on' if request.is_secure() else 'off',
        #'http_host': request.META['HTTP_HOST'],
        'http_host': http_host,
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy()
    }
    return result

@csrf_exempt
def saml(request):
    req = prepare_django_request(request)
    if request.session.pop('slo', None):
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
        result = HttpResponseRedirect(auth.login()) 
        return result

    elif 'acs' in req['get_data']:
        auth.process_response()
        errors = auth.get_errors()
        next = request.session.get('next_saml', None)

        if not errors:
            attributes = auth.get_attributes()
            name_id = auth.get_nameid()
            session_index = auth.get_session_index()
            
            request.session['samlUserdata'] = attributes
            request.session['samlNameId'] = name_id
            request.session['samlSessionIndex'] = session_index

            email = attributes.get('email')[0]
            extid = check_externalid(request, shortname=idp_shortname, externalid=email)
            if not extid:
                if next:
                    #connect SAML user with User
                    #don't convert next string yet
                    goto = settings.LOGIN_URL + '?next=' + next
                else:
                    goto = settings.LOGIN_URL
                return redirect(goto)

            #now is time to convert next string to original value
            try:
                next = next.replace("%26", "&")
            except AttributeError:
                pass

            user = User.objects.get(pk=extid.userid.pk)

            pl = PleioLoginView()
            pl.post_login_process(request, user, next=next)
            if next:
                return redirect(next)

        if next:
            goto = settings.LOGIN_REDIRECT_URL + '?next=' + next
        else:
            goto = settings.LOGIN_REDIRECT_URL

        return redirect(goto)

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


def check_externalid(request, **kwargs):
    shortname=kwargs.get('shortname') 
    externalid=kwargs.get('externalid')
    try:
        idp = IdentityProvider.objects.get(shortname=shortname)
    except IdentityProvider.DoesNotExist:
        return None

    request.session['samlConnect'] = True

    try:
        extid = ExternalIds.objects.get(identityproviderid=idp, externalid=externalid)
    except ExternalIds.DoesNotExist:
        extid = None

    return extid


def connect_and_login(request):
    next = request.session.get('next_saml', None)
    #now is time to convert next string to original value
    try:
        next = next.replace("%26", "&")
    except AttributeError:
        pass

    extid = connect(request)
    if not extid:
        if next:
            goto = settings.LOGIN_URL + '?next=' + next
        else:
            goto = settings.LOGIN_URL
        return redirect(goto)

    user = User.objects.get(pk=extid.userid.pk)

    pl = PleioLoginView()
    pl.post_login_process(request, user, next=next)

    if next:
        return redirect(next)
    else:
        return redirect(settings.LOGIN_REDIRECT_URL) 


def connect(request, user_email=None):
    idp_shortname = request.session.get('idp') or None
    if not idp_shortname:
        return None        

    samlUserdata = request.session.get('samlUserdata') or None
    if samlUserdata:       
        email = samlUserdata.get('email')[0] or None
    if not email:
        return redirect(settings.LOGIN_REDIRECT_URL)        
    if not user_email:
        user_email = email

    try:
        idp = IdentityProvider.objects.get(shortname=idp_shortname)
    except IdentityProvider.DoesNotExist:
        return None 

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:      
        user = User.objects.create_user(
            email=email,
            name=email,
            password=signing.dumps(obj=email),
            accepted_terms=True,
            receives_newsletter=False
            )
        user.is_active=True
        user.save()
        user.send_set_password_activation_token()

    try:
        extid = ExternalIds.objects.get(identityproviderid=idp, externalid=email)
    except ExternalIds.DoesNotExist:
        extid= ExternalIds.objects.create(
            identityproviderid=idp,
            externalid=email,
            userid=user
        )

    return extid


def set_new_password(request, activation_token=None):
    if request.method == 'POST':
        user = request.user
        form = SetPasswordForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            user.set_password(data['new_password2'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Password changed'), extra_tags='password')
            return redirect('profile')
        else:
            return render(request, 'set_new_password.html', { 'form': form })
    else:
        user = User.set_new_password(None, activation_token)
        if not user:
            return redirect(settings.LOGIN_URL)
        auth_login(request, user)
        form = SetPasswordForm()
        return render(request, 'set_new_password.html', { 'form': form })

    return redirect(settings.LOGIN_URL)



def show_connections(request):
    connections = ExternalIds.objects.filter(userid=request.user)    

    return render(request, 'show_connections.html', {'connections': connections})



def delete_connection(request, pk=None):
    if pk:
        try:
            connection = ExternalIds.objects.get(pk=pk).delete()
        except:
            pass

    return redirect('saml_connections')

