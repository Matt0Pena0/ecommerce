from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

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
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        try:
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            messages.success(
                self.request,
                "Usuario creado correctamente. Inicie sesión.")
        except IntegrityError:
            form.add_error("Error en la creación del usuario.")
            return self.form_invalid(form)

        return super().form_valid(form)


# Cambio de contraseña
class BasePasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return super().form_valid(form)


# Recuperación de contraseña
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView)


class BasePasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Se ha enviado un email con instrucciones para recuperar tu contraseña.")
        return super().form_valid(form)


class BasePasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class BasePasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Tu contraseña ha sido restablecida correctamente.")
        return super().form_valid(form)


class BasePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
