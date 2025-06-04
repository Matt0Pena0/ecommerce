from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


User = get_user_model()
class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=140, label="Nombre de usuario")
    first_name = forms.CharField(max_length=140, label="Nombre")
    last_name = forms.CharField(max_length=140, label="Apellido")
    email = forms.EmailField(max_length=140, label="Email")

    password1 = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repite tu contraseña")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2 and password1 != "":
            raise forms.ValidationError("Las contraseñas no coinciden")

        if password2 != "":
            validate_password(password2)

        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")

        return email