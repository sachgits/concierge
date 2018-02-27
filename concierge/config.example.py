"""
Django settings for concierge project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#directory containing settings and Server Provider certificate for SAML
SAML_FOLDER = os.path.join(BASE_DIR, 'saml/configuration')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

FROM_EMAIL = 'noreply@pleio.nl'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25

TIME_ZONE = 'Europe/Amsterdam'

EXTERNAL_HOST = 'https://www.concierge.nl/'
EMAIL_LOGO = '/images/email-logo.png'

SITE_TITLE = 'Pleio account'
SITE_LOGO = 'images/logo.svg'
SITE_FAVICON = 'images/favicon.png'

#This setting controls whether an image should be displayed when a user is also a member of other group(s) than "Any"
SHOW_GOVERNMENT_BADGE = True

# Send users a warning message when suspicious behaviour on their account occurs, e.g. a login on the account from a new (unknown) location.
SEND_SUSPICIOUS_BEHAVIOR_WARNINGS = True

#Google reCAPTCHA Will be present on login page when from that IP adress more than RECAPTCHA_NUMBER_INVALID_LOGINS during the last RECAPTCHA_MINUTES_THRESHOLD have occurred.
RECAPTCHA_MINUTES_THRESHOLD = 30
RECAPTCHA_NUMBER_INVALID_LOGINS = 10 

# Request an API key at https://developers.google.com/recaptcha/ for reCAPTCHA validation.

# With the following test keys, you will always get No CAPTCHA and all verification requests will pass.
GOOGLE_RECAPTCHA_SITE_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

SAML2_SP = {
    "entityId": "http://127.0.0.1:8000/saml/metadata",
    "assertionConsumerService": {
        "url": "http://127.0.0.1:8000/saml/?acs",
        "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    },
    "singleLogoutService": {
        "url": "http://127.0.0.1:8000/saml/?sls",
        "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    },
    "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
    "x509cert": "",
    "privateKey": ""
}
SAML_IDP_BINDING = "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"

# Setting CELERY_ALWAYS_EAGER to "True"  will make task being executed locally in the client, not by a worker.
# Always use "False" in production environment.
CELERY_ALWAYS_EAGER = True | False

BROKER_URL = "amqp://localhost"