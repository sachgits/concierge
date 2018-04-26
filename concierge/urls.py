"""concierge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.views.decorators.clickjacking import xframe_options_exempt
from oauth2_provider import views as oauth2_views
from saml import views as saml_views
from api import views as api_views
from django.contrib import admin
from core import views
from core.class_views import PleioLoginView, PleioSessionDeleteView, PleioSessionDeleteOtherView
from django.views.i18n import JavaScriptCatalog

class DecoratedURLPattern(RegexURLPattern):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedURLPattern, self).resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


class DecoratedRegexURLResolver(RegexURLResolver):
    def resolve(self, *args, **kwargs):
        result = super(DecoratedRegexURLResolver, self) \
            .resolve(*args, **kwargs)
        if result:
            result.func = self._decorate_with(result.func)
        return result


def decorated_includes(func, includes):
    """
    Include URLconf from module but apply the specified decorator to each.
    """
    urlconf_module, app_name, namespace = includes
    urlconf_urls = urlconf_module.urlpatterns

    for item in urlconf_urls:
        if isinstance(item, RegexURLPattern):
            item.__class__ = DecoratedURLPattern
            item._decorate_with = func

        elif isinstance(item, RegexURLResolver):
            item.__class__ = DecoratedRegexURLResolver
            item._decorate_with = func

    return urlconf_module, app_name, namespace


legacy_urls = [
    url(r'^mod/profile/icondirect.php$', views.avatar, name='avatar_legacy'),
    url(r'^action/logout$', views.logout, name='logout_legacy')
]

urls = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register/complete/$', views.register_complete, name='register_complete'),
    url(r'^register/activate/(?P<activation_token>[-:\w]+)/$', views.register_activate, name='register_activate'),
    url(r'^change-email/$', views.change_email, name='change_email'),
    url(r'^change-email/activate/(?P<activation_token>[-:\w]+)/$', views.change_email_activate, name='change_email_activate'),
    url(r'^htmlsnippet/(?P<page_name>[\w-]+)/$', views.html_snippet, name='html_snippet'),
    url(r'^securitypages/(?P<page_action>[\w-]+)/$', views.security_pages, name='security_pages'),
    url(r'^securitypages/$', views.security_pages, name='security_pages'),
    url(r'^password_reset/$', auth_views.password_reset, { 'template_name': 'password_reset.html', 'subject_template_name': 'emails/reset_password_subject.txt', 'email_template_name': 'emails/reset_password.txt', 'html_email_template_name': 'emails/reset_password.html' }, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, { 'template_name': 'password_reset_done.html' }, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, { 'template_name': 'password_reset_confirm.html' }, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, { 'template_name': 'password_reset_complete.html' }, name='password_reset_complete'),
    url(r'^login/(?P<login_step>[\w-]+)/$', PleioLoginView.as_view(), name='login'),
    url(r'^login/$', PleioLoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^delete-account/$', views.delete_account, name='delete_account'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^account/sessions/other/delete/$', view=PleioSessionDeleteOtherView.as_view(), name='session_delete_other'),
    url(r'^account/sessions/(?P<pk>\w+)/delete/$', view=PleioSessionDeleteView.as_view(), name='session_delete'),
    url(r'^oauth/v2/authorize$', oauth2_views.AuthorizationView.as_view(), name='authorize'),
    url(r'^oauth/v2/token$', oauth2_views.TokenView.as_view(), name='token'),
    url(r'^oauth/v2/revoke_token$', oauth2_views.RevokeTokenView.as_view(), name='revoke-token'),
    url(r'^api/users/me$', api_views.me, name='me'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home')
]

tf_urls = [
    url(r'', include('two_factor.urls', 'two_factor'))
]
us_urls = [
    url(r'', include('user_sessions.urls', 'user_sessions'))
]
oidc_urls = [
    url(r'^openid/', decorated_includes(
      xframe_options_exempt,
      include('oidc_provider.urls', namespace='oidc_provider')
    ))
]
django_urls = [
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]
saml_urls = [
    url(r'^saml/$', saml_views.saml, name='saml'),
    url(r'^saml/attrs/$', saml_views.attrs, name='saml-attrs'),
    url(r'^saml/metadata/$', saml_views.metadata, name='saml-metadata'),
    url(r'^saml/connect/$', saml_views.connect_and_login, name='saml-connect'),
    url(r'^saml/set_new_password/(?P<activation_token>[-:\w]+)/$', saml_views.set_new_password, name='set_new_password'),
    url(r'^saml/connections/$', saml_views.show_connections, name='saml_connections'),
    url(r'^saml/connection_delete/(?P<pk>\w+)/$', saml_views.delete_connection, name='saml_connection_delete'),
]
urlpatterns = legacy_urls + urls + tf_urls + us_urls + oidc_urls + django_urls + saml_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
