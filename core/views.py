from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserProfileForm, PleioTOTPDeviceForm, ChangePasswordForm, DeleteAccountForm, LegalTextForm
from .models import User, ResizedAvatars, PreviousLogins, PleioLegalText
from django.http import JsonResponse
from django.urls import reverse
from base64 import b32encode
from binascii import unhexlify
from django_otp.util import random_hex
import django_otp
from django.conf import settings
from saml.models import IdentityProvider, IdpEmailDomain
from urllib.parse import urljoin
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, update_session_auth_hash
from two_factor.views import ProfileView
from user_sessions.views import SessionListView
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages
from django.template.response import TemplateResponse
from django.contrib.auth import password_validation
from core.class_views import PleioBackupTokensView, PleioSessionListView, PleioProfileView
from two_factor.views.profile import DisableView


def home(request):
    if request.user.is_authenticated():
        return redirect('profile')

    return redirect('login')


def logout(request):
    #If user has logged in via SAML IDP verification, the user has to log out at SAML IDP first if the IDP supports / allows that
    # IdentityProvider.sloId either contains url for single logout or is empty 
    if request.session.pop('samlLogin', None):
        idp = request.session.get('idp', None)
        if idp:
            idp_row = IdentityProvider.objects.get(shortname=idp)
            if idp_row.perform_slo:
                try:
                    slo = idp_row.sloId
                except IdentityProvider.DoesNotExist:
                    slo = None
            else:
                slo = None
        if slo:
            request.session['slo'] = 'slo'
            return redirect('saml_slo')

    #If needed the account can be deleted now that user has been logged out at SAML IDP
    if request.session.pop('DeleteAccountPending', None):
        request.user.delete()

    auth.logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated():
        return redirect('profile')

    legal_text = PleioLegalText.get_legal_text(request, page_name='terms')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(
                    name=data['name'],
                    email=data['email'],
                    password=data['password2'],
                    accepted_terms=data['accepted_terms'],
                    receives_newsletter=data['receives_newsletter']
                )
            except:
                user = User.objects.get(email=data['email'])

            if not user.is_active:
                user.send_activation_token()

            return redirect('register_complete')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'legal_text': legal_text})


def register_complete(request):
    return render(request, 'register_complete.html')


def register_activate(request, activation_token=None):
    if request.user.is_authenticated():
        return redirect('profile')

    user = User.activate_user(None, activation_token)

    if user:
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('profile')

    return render(request, 'register_activate.html')


def change_email(request):
    user = request.user
    user.send_change_email_activation_token()

    return redirect('profile')

def change_email_activate(request, activation_token=None):
    user = User.change_email(None, activation_token)

    if user:
        messages.success(request, _('Email address changed'), extra_tags='email')

    return redirect('profile')

@login_required
def profile(request):
    if request.method == 'POST':
        new_email_save = request.user.new_email
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            data = form.cleaned_data
            new_email = data['new_email']
            user = form.save()
            user.new_email = new_email
            user.save()
            if new_email and (new_email != new_email_save):
                change_email(request)
            form = UserProfileForm(instance=request.user)
            messages.success(request, _('Profile changed'), extra_tags='profile')
    else:
        form = UserProfileForm(instance=request.user)

    if request.user.new_email:
        text_change_pending = _('There is a pending change of your email to ')
    else:
        text_change_pending = None

    return render(request, 'profile.html', {'form': form, 'text_change_pending': text_change_pending, 'text_email': request.user.new_email})


def avatar(request):
    #DEFAULT_AVATAR = '/static/images/gebruiker.svg'
    avatar_size = request.GET.get('size')
    DEFAULT_AVATAR = urljoin('https://www.pleio.nl/_graphics/icons/user/', str('default' +avatar_size + '.gif'))

    user = User.objects.get(id=request.GET.get('guid'))

    try:
        user = User.objects.get(id=int(request.GET['guid']))
        if user.avatar:
            try:
                resized_avatars = ResizedAvatars.objects.get(user=user)
                if avatar_size == 'large':
                    avatar = resized_avatars.large
                elif avatar_size == 'small':
                    avatar = resized_avatars.small
                elif avatar_size == 'tiny':
                    avatar = resized_avatars.tiny
                elif avatar_size == 'topbar':
                    avatar = resized_avatars.topbar
                else: #when no size is requested, medium will be served
                    avatar = resized_avatars.medium

                return redirect('/media/' + str(avatar))
            except ResizedAvatars.DoesNotExist:
                pass
    except User.DoesNotExist:
        pass

    return redirect(DEFAULT_AVATAR)


def legal_pages(request, page_name=None, language_code=None):
    legal_text = PleioLegalText.get_legal_text(request, page_name=page_name, language_code=language_code)

    if request.user.is_authenticated:
        return render(request, 'legal_text_account.html', {'legal_text': legal_text})
    else:
        return render(request, 'legal_text.html', {'legal_text': legal_text})

@login_required
def security_pages(request, page_action=None):

    return render(request, 'security_pages.html', {
        'pass_reset_form': change_password_form(request, page_action),
        '2FA': two_factor_form(request, page_action),
        'user_session_form': user_sessions_form(request)
    })

def change_password_form(request, page_action):
    if page_action == 'change-password':
        user = request.user
        form = ChangePasswordForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            user.set_password(data['new_password2'])
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Password has been changed successfully.'), extra_tags='password')
    else:
        form = ChangePasswordForm()

    return form

def two_factor_form(request, page_action):
    two_factor_authorization =  {}
    if page_action == '2fa-setup':
        key = random_hex(20).decode('ascii')
        rawkey = unhexlify(key.encode('ascii'))
        b32key = b32encode(rawkey).decode('utf-8')

        request.session['tf_key'] = key
        request.session['django_two_factor-qr_secret_key'] = b32key

        two_factor_authorization = ({
            'form': PleioTOTPDeviceForm(key=key, user=request.user),
            'QR_URL': reverse('two_factor:qr')
        })
        two_factor_authorization['state'] = 'setup'

    elif page_action == '2fa-setupnext':
        key = request.session.get('tf_key')
        form = PleioTOTPDeviceForm(data=request.POST, key=key, user=request.user)
        if form.is_valid():
            device = form.save()
            django_otp.login(request, device)
            two_factor_authorization['default_device'] = True
            two_factor_authorization['show_state'] = True
        else:
            two_factor_authorization['form'] = form
            two_factor_authorization['QR_URL'] = reverse('two_factor:qr')
            two_factor_authorization['state'] = 'setup'

    elif page_action == '2fa-disable':
        two_factor_authorization = DisableView.as_view(template_name='security_pages.html')(request).context_data
        two_factor_authorization['state'] = 'disable'

    elif page_action == '2fa-disableconfirm':
        two_factor_authorization = DisableView.as_view(template_name='security_pages.html')(request)
        two_factor_authorization['state'] = 'default'
        two_factor_authorization['show_state'] = 'true'

    elif page_action == '2fa-showcodes':
        two_factor_authorization = PleioBackupTokensView.as_view(template_name='backup_tokens.html')(request).context_data
        two_factor_authorization['default_device'] = 'true'
        two_factor_authorization['state'] = 'codes'
        two_factor_authorization['show_state'] = 'true'

    elif page_action == '2fa-generatecodes':
        two_factor_authorization = PleioBackupTokensView.as_view(template_name='security_pages.html')(request).context_data
        two_factor_authorization['default_device'] = 'true'
        two_factor_authorization['show_state'] = 'true'
        two_factor_authorization['state'] = 'codes'

    else:
        two_factor_authorization = PleioProfileView.as_view(template_name='security_pages.html')(request).context_data
        two_factor_authorization['state'] = 'default'
        two_factor_authorization['show_state'] = 'true'

    return two_factor_authorization

def user_sessions_form(request):
    user_sessions = PleioSessionListView.as_view(template_name='security_pages.html')(request).context_data

    return user_sessions['object_list']

@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            #delay actual deleting of the account to preserve the session needed to log out at SAML IDP
            request.session['DeleteAccountPending'] = True
            messages.success(request, _('Account deleted'), extra_tags='account_deleted')
            return redirect(settings.LOGOUT_REDIRECT_URL)
    else:
        form = DeleteAccountForm(user=request.user)
        

    return render(request, 'delete_account.html', { 'form': form })

def get_user_and_idp(request):
    email = request.POST.get('email')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    idp = None

    try:
        email_domain = email.split('@')[1]
        try:
            idp = IdpEmailDomain.objects.get(email_domain=email_domain).identityprovider.shortname
        except IdpEmailDomain.DoesNotExist:
            pass
    except IndexError:
        pass

    return JsonResponse({
        "user_exists": user != None,
        "idp": idp
    })