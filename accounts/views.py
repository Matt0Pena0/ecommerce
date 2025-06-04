from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from django.db import IntegrityError

from .forms import UserRegisterForm


# Inicio de sesión
class BaseLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("core:home") 

    def get_success_url(self):
        return self.success_url


# Cierre de sesión
class BaseLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


# Registro
User = get_user_model()
class BaseUserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")  # Redirige al login luego de registrarse

    def form_valid(self, form):
        # Creamos el usuario
        try:
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            messages.success(self.request, "Usuario creado correctamente. Inicie sesión.")
        except IntegrityError:
            form.add_error("Error en la creación del usuario.")
            return self.form_invalid(form)

        return super().form_valid(form)