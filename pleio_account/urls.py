"""pleio_account URL Configuration

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
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register/complete/$', views.register_complete, name='register_complete'),
    url(r'^register/activate/(?P<activation_key>[-:\w]+)/$', views.register_activate, name='register_activate'),
    url(r'^password_reset/$', auth_views.password_reset, { 'template_name': 'password_reset.html' }, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, { 'template_name': 'password_reset_done.html' }, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, { 'template_name': 'password_reset_confirm.html' }, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, { 'template_name': 'password_reset_complete.html' }, name='password_reset_complete'),
    url(r'^login/$', auth_views.login, { 'template_name': 'login.html' }, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home')
]
