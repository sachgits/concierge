# Pleio account
This is the Pleio microservice used for handling user registration, login and SAML2 SSO. It is based on [Django project](https://www.djangoproject.com/) and handles login througout the Pleio ecosystem using OAuth2.

## Setup development environment
To setup the development environment, run the following commands in the :

    mkvirtualenv pleio_account
    pip install -r requirements.txt
    npm install

## Start the development environment

    npm run watch & python manage.py runserver localhost:8001

## Generate new translations
We use the standard [i18n toolset of Django](https://docs.djangoproject.com/en/1.10/topics/i18n/). To add new translations to the source files use:

    python manage.py makemessages

To compile the translations use:

    python manage.py compilemessages

On OSX first make sure gettext (> 0.14) is installed and linked using:

    brew install --force gettext
    brew link --force gettext

## Run tests
To run the accompanied test suite use:

    python manage.py test
