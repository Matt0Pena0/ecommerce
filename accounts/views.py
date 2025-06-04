from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


# Login
class BaseLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("core:home") 

    def get_success_url(self):
        return self.success_url

class BaseLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")