
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import CustomUserAuthenticationForm, UserRegisterForm


# Inicio de sesión
class BaseLoginView(LoginView):
    """
    Vista personalizada para el inicio de sesión de usuarios, que hereda de 
        :view: `LoginView`.

    - Usa un formulario de autenticación personalizado, para la personalización de `error_messages`.
        :form: `CustomUserAuthenticationForm`
    
    - Redirige a  automáticamente si el usuario ya está autenticado.
        :template: `accounts/Login.html`.
    """

    template_name = "accounts/Login.html"
    authentication_form = CustomUserAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("core:home")

    def get_success_url(self):
        return self.success_url


# Cierre de sesión
class BaseLogoutView(LogoutView):
    """
    Vista base, herda de:
        :view: `LogoutView`

    Redirige a la vista de Login:
        :view: `accounts.BaseLoginView`
    """

    next_page = reverse_lazy("accounts:login")


# Registro
User = get_user_model()

class BaseUserRegisterView(FormView):
    """
    Vista personalizada para registrar un nuevo usuario, hereda de:
        :form: `accounts.forms.FormView`
    """

    form_class = UserRegisterForm
    template_name = "accounts/Register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        messages.success(
                self.request, "Usuario creado correctamente. Inicie sesión."
            )
        return super().form_valid(form)


# Cambio de contraseña
class BasePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change/Change.html"
    success_url = reverse_lazy("accounts:password_change:complete")

    def form_invalid(self, form):
        messages.error(self.request, "El email ingresado no es válido o no está registrado.")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return super().form_valid(form)


# Recuperación de contraseña
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)


class BasePasswordResetView(PasswordResetView):
    """
    Flujo de recuperación de contraseña:

    - La :view: `accounts.BasePasswordResetView`: recibe el correo para enviar los pasos de recuperación.
        :template: `accounts/password_reset/Reset.html`

    - La :view: `accounts.BasePasswordResetDoneView`: confirma que el correo fue enviado.
        :template: `accounts/password_reset/Done.html`

    - La :view: `accounts.BasePasswordResetConfirmView`: permite ingresar nueva contraseña.
        :template: `accounts/password_reset/Confirm.html`

    - La :view: `accounts.BasePasswordResetCompleteView`: confirma que la contraseña fue restablecida.
        :template: `accounts/password_reset/Complete.html`
    """

    template_name = "accounts/password_reset/Reset.html"
    email_template_name = "accounts/password_reset/email.html"
    subject_template_name = "accounts/password_reset/subject.txt"
    success_url = reverse_lazy("accounts:password_reset:done")

    def form_invalid(self, form):
        messages.error(self.request, "El email ingresado no es válido o no está registrado.")
        return super().form_invalid(form) 

    def form_valid(self, form):
        messages.success(
            self.request,
            "Correo de recuperación enviado correctamente.",
        )
        return super().form_valid(form)


class BasePasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset/Done.html"


class BasePasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset/Confirm.html"
    success_url = reverse_lazy("accounts:password_reset:complete")

    def form_valid(self, form):
        messages.success(
            self.request, "Tu contraseña ha sido restablecida correctamente."
        )
        return super().form_valid(form)


class BasePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset/Complete.html"
