from django.urls import path

from accounts.views import BaseLoginView, BaseLogoutView, BaseUserRegisterView


app_name = "accounts"

urlpatterns = [
    path("login/", BaseLoginView.as_view(), name="login"),
    path("logout/", BaseLogoutView.as_view(), name="logout"),
    path("register/", BaseUserRegisterView.as_view(), name="register"),
]


# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']