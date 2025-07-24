
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import CustomUserAuthenticationForm, UserRegisterForm


# Inicio de sesión
class BaseLoginView(LoginView):
    template_name = "accounts/Login.html"
    authentication_form = CustomUserAuthenticationForm
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
    template_name = "accounts/Register.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
        messages.success(
                self.request, "Usuario creado correctamente. Inicie sesión."
            )
        return super().form_valid(form)


# Cambio de contraseña
class BasePasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/password_change/Change.html"
    success_url = reverse_lazy("accounts:password_change:done")

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return super().form_valid(form)


# Recuperación de contraseña
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)


class BasePasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset/Reset.html"
    email_template_name = "accounts/password_reset/email.html"
    subject_template_name = "accounts/password_reset/subject.txt"
    success_url = reverse_lazy("accounts:password_reset:done")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Correo enviado correctamente.",
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
