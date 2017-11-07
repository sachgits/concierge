from .forms import PleioAuthenticationForm, PleioAuthenticationTokenForm
from .views import check_users_previous_logins
from two_factor.forms import TOTPDeviceForm, BackupTokenForm
from two_factor.views.core import LoginView, SetupView

class PleioLoginView(LoginView):
    template_name = 'login.html'

    form_list = (
        ('auth', PleioAuthenticationForm),
        ('token', PleioAuthenticationTokenForm),
        ('backup', BackupTokenForm),
    )

    def done(self, form_list, **kwargs):
        if self.request.POST.get('auth-is_persistent'):
            self.request.session.set_expiry(30 * 24 * 60 * 60)
        else:
            self.request.session.set_expiry(0)

        user = self.get_user()

        try:
            device_id = self.request.COOKIES['device_id']
        except:
            device_id = None

        check_users_previous_logins(self.request, user, device_id)

        return LoginView.done(self, form_list, **kwargs)
