from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView, LoginView
from users.forms import UserLoginForm
from django.contrib.auth import login as auth_login


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'cms/layout.html'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect('/home/')


class UserLogout(LogoutView):
    next_page = 'home'
