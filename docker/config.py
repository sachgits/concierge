import os
import sys

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.getenv('BASE_DIR')

#directory containing settings and Server Provider certificate for SAML
SAML_FOLDER = os.getenv('SAML_FOLDER')

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOST')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'NAME': os.getenv('DB_NAME'),
    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

STATIC_ROOT = '/app/static'

LANGUAGE_CODE = 'nl-nl'

TIME_ZONE = 'Europe/Amsterdam'

STATIC_ROOT = '/app/static'

EXTERNAL_HOST = os.getenv('EXTERNAL_HOST', 'http://localhost:8000')
EMAIL_LOGO = os.getenv('EMAIL_LOGO', 'images/email-logo.png')

SITE_TITLE = os.getenv('SITE_TITLE', 'Pleio')
SITE_LOGO = os.getenv('SITE_LOGO', 'images/logo.svg')
SITE_FAVICON = os.getenv('SITE_FAVICON', 'images/favicon.svg')

SEND_SUSPICIOUS_BEHAVIOR_WARNINGS = os.getenv('SEND_SUSPICIOUS_BEHAVIOR_WARNINGS')

DEFAULT_FROM_EMAIL = os.getenv('FROM_EMAIL')
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL')


# Used for testing without SMTP
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')

SITE_URL = os.getenv('SITE_URL', None)
CORS_ORIGIN_WHITELIST = os.getenv('CORS_ORIGIN_WHITELIST', '').split(',')

GOOGLE_RECAPTCHA_SITE_KEY = os.getenv('GOOGLE_RECAPTCHA_SITE_KEY')
GOOGLE_RECAPTCHA_SECRET_KEY = os.getenv('GOOGLE_RECAPTCHA_SECRET_KEY')

SAML2_SP = {
    "entityId": os.getenv("EXTERNAL_HOST") + "/saml/metadata",
    "assertionConsumerService": {
        "url": os.getenv("EXTERNAL_HOST") + "/saml/?acs",
        "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
    },
    "singleLogoutService": {
        "url": os.getenv("EXTERNAL_HOST") + "/saml/?sls",
        "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
    },
    "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
    "x509cert": os.getenv("SAML_SP_X509CERT"),
    "privateKey": os.getenv("SAML_SP_PRIVATEKEY")
}

CELERY_ALWAYS_EAGER = True
CELERY_BROKER_URL = os.getenv('MESSAGE_QUEUE')