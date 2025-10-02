import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


# Test para casos de autenticación
@pytest.mark.django_db
def test_login_success(client):
    user = User.objects.create_user(username="testuser", password="securepassword")
    response = client.post(reverse("accounts:login"), {
        "username": "testuser",
        "password": "securepassword",
    })
    assert response.status_code == 302
    assert response.url == reverse("core:home")


@pytest.mark.django_db
def test_login_fail(client):
    response = client.post(reverse("accounts:login"), {
        "username": "wronguser",
        "password": "wrongpass",
    })
    assert response.status_code == 200
    assert "form" in response.context
    assert response.context["form"].errors


@pytest.mark.django_db
def test_logout(client):
    user = User.objects.create_user(username="testuser", password="securepassword")
    client.login(username="testuser", password="securepassword")
    response = client.post(reverse("accounts:logout"))
    assert response.status_code == 302
    assert response.url == reverse("accounts:login")


def test_login_form_display(client):
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200
    assert "csrfmiddlewaretoken" in response.content.decode()


# Test para casos de registro de usuario
@pytest.mark.django_db
def test_register_success(client):
    response = client.post(reverse("accounts:register"), {
        "username": "nuevo_user",
        "first_name": "Nuevo",
        "last_name": "Usuario",
        "email": "nuevo@example.com",
        "password1": "UnaContraseñaSegura123",
        "password2": "UnaContraseñaSegura123",
    })

    assert response.status_code == 302
    assert response.url == reverse("accounts:login")
    assert User.objects.filter(username="nuevo_user").exists()


@pytest.mark.django_db
def test_register_fail_duplicate_username(client):
    User.objects.create_user(username="usuario_existente", email="test@example.com", password="123")

    response = client.post(reverse("accounts:register"), {
        "username": "usuario_existente",
        "first_name": "Test",
        "last_name": "Usuario",
        "email": "otro@example.com",
        "password1": "UnaContraseña123",
        "password2": "UnaContraseña123",
    })

    assert response.status_code == 200
    assert "form" in response.context
    assert "username" in response.context["form"].errors


@pytest.mark.django_db
def test_register_fail_duplicate_email(client):
    User.objects.create_user(username="usuario_existente", email="email@repetido.com", password="123")

    response = client.post(reverse("accounts:register"), {
        "username": "usuario_inexistente",
        "first_name": "Test",
        "last_name": "Usuario",
        "email": "email@repetido.com",
        "password1": "UnaContraseña123",
        "password2": "UnaContraseña123",
    })

    assert response.status_code == 200
    assert "form" in response.context
    assert "email" in response.context["form"].errors


@pytest.mark.django_db
def test_register_fail_password_mismatch(client):
    response = client.post(reverse("accounts:register"), {
        "username": "user_password_fail",
        "first_name": "User",
        "last_name": "Fail",
        "email": "fail@example.com",
        "password1": "Contraseña123",
        "password2": "ContraseñaDiferente456",
    })

    assert response.status_code == 200
    assert "form" in response.context
    assert "password2" in response.context["form"].errors
