from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.contrib import auth
from django.core import mail
from django.test.client import RequestFactory
from .helpers import generate_activation_token, activate_user, accept_previous_logins, generate_acceptation_token
from .models import User, PreviousLogins
from .views import check_users_previous_logins

class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name="John", email="john@user.com", password="GkCyKt6iWJVi")
        self.superuser = User.objects.create_superuser(name="John", email="john@superuser.com", password="LZwHZucJj9JD")

        self.factory = RequestFactory()

    def test_generated_username(self):
        """ Make sure a correct unique username is generated for each user """
        self.assertEqual(self.user.username, "john")
        self.assertEqual(self.superuser.username, "john-1")

    def test_normal_user_is_inactive_when_created(self):
        """ Make sure a (normal) user is in inactive state when being created """
        self.assertIs(self.user.is_active, False)

    def test_superuser_is_active_when_created(self):
        """ Make sure a superuser is in active state when being created """
        self.assertIs(self.superuser.is_active, True)

    def test_login_with_email(self):
        """ Make sure a user can login with email and password """
        invalid_login = auth.authenticate(username="john@superuser.com", password="asdf")
        valid_login = auth.authenticate(username="john@superuser.com", password="LZwHZucJj9JD")   
        self.assertEqual(invalid_login, None)
        self.assertEqual(valid_login, self.superuser)

    def test_account_activation(self):
        """ Test an account can be activated and login by using the activation token """
        request = self.factory.get("/")
        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)

        activation_token = generate_activation_token(self.user.email)
        activate_user(activation_token)

        self.user.refresh_from_db()

        self.assertIs(self.user.is_active, True)
        self.assertEqual(request.user, self.user)

    def test_send_email_suspicious_login(self):
        """ Test  """
        request = self.factory.get("/")

        middleware = SessionMiddleware()
        middleware.process_request(request)

        request.session.ip = "8.247.18.183" #www.ziggo.nl an existing ip address
        request.session.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.75 Chrome/62.0.3202.75 Safari/537.36"

        device_id = "yj9zaceo1v6i6uw4hr0k2h8qs11zvjgd"

        result = check_users_previous_logins(request, self.user, device_id)
        self.assertIs(result, False)#no confirmed previous login found, so an email has been sent

        acceptation_token = generate_acceptation_token(device_id)
        accept_previous_logins(request, acceptation_token)

        result = check_users_previous_logins(request, self.user, device_id)
        self.assertIs(result, True)#confirmed previous login found, ho email has been sent


