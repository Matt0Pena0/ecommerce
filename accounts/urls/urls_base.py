from django.urls import include, path

from accounts.views import BaseLoginView, BaseLogoutView, BaseUserRegisterView

app_name = "accounts"

urlpatterns = [
    path("login/", BaseLoginView.as_view(), name="login"),
    path("logout/", BaseLogoutView.as_view(), name="logout"),
    path("register/", BaseUserRegisterView.as_view(), name="register"),
    path(
        "password/change/",
        include(
            ("accounts.urls.password_change", "accounts"),
            namespace="password_change"
        ),
    ),
    path(
        "password/reset/",
        include(
            ("accounts.urls.password_reset", "accounts"),
            namespace="password_reset"
        ),
    ),
]
