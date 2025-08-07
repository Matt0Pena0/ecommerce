from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class CustomUserAuthenticationForm(AuthenticationForm):
    """
    Formulario base, que hereda de :class: `django.contrib.auth.forms.AuthenticationForm`, se modifica `error_messages` para personalizar el mensaje
    """
    error_messages = {
        "invalid_login": "Por favor, introduzca un nombre de usuario y contraseña válidos.",
        "inactive": "Esta cuenta está inactiva.",
    }


class UserRegisterForm(forms.Form):
    """
    Formulario de registro de usuario.

    Incluye campos básicos como nombre, apellido, email y contraseña. 
    Realiza validaciones personalizadas para evitar duplicados y asegurar la seguridad de la contraseña.

    :fields:
        - ``username``: Nombre de usuario único.
        - ``first_name`` / ``last_name``: Nombre y apellido del usuario.
        - ``email``: Correo electrónico único.
        - ``password1`` / ``password2``: Contraseña y confirmación.

    :validations:
        - Verifica que las contraseñas coincidan.
        - Aplica validación de seguridad con :func:`validate_password`.
        - Verifica unicidad de nombre de usuario y email.
    """

    username = forms.CharField(max_length=140, label="Nombre de usuario")
    first_name = forms.CharField(max_length=140, label="Nombre")
    last_name = forms.CharField(max_length=140, label="Apellido")
    email = forms.EmailField(max_length=140, label="Email")
    direccion = forms.CharField(max_length=100, label= "Dirección")

    password1 = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    password2 = forms.CharField(
        widget=forms.PasswordInput(), label="Repite tu contraseña"
    )

    def clean_password2(self):
        """
        Valida que las contraseñas coincidan y cumplan con los requisitos de seguridad.

        :return: Contraseña validada.
        :raises ValidationError: Si las contraseñas no coinciden o no cumplen con los requisitos.
        """

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2 and password1 != "":
            raise forms.ValidationError("Las contraseñas no coinciden")

        if password2 != "":
            validate_password(password2)

        return password2

    def clean_username(self):
        """
        Valida que el username no esté en uso.

        :return: username.
        :raises ValidationError: Si ya hay un usuario igual registrado en :model: `models.UsuarioBase`
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")

        return username

    def clean_email(self):
        """
        Valida que el email no esté en uso.

        :return: email.
        :raises ValidationError: Si ya hay un email igual registrado en :model: `models.UsuarioBase`
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")

        return email
