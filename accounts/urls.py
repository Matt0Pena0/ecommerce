from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView

from accounts.views import (
    BaseLoginView, BaseLogoutView, BaseUserRegisterView, BasePasswordChangeView,
    BasePasswordResetView, BasePasswordResetDoneView, BasePasswordResetConfirmView, BasePasswordResetCompleteView
)

app_name = "accounts"

urlpatterns = [
    path("login/", BaseLoginView.as_view(), name="login"),
    path("logout/", BaseLogoutView.as_view(), name="logout"),
    path("register/", BaseUserRegisterView.as_view(), name="register"),
    path("password/change/", BasePasswordChangeView.as_view(), name="password_change"),
    path("password/change/done/", PasswordChangeDoneView.as_view(template_name="accounts/password_change_done.html"), name="password_change_done"),

]

urlpatterns += [
    path("password/reset/", BasePasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", BasePasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password/reset/confirm/<uidb64>/<token>/", BasePasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/complete/", BasePasswordResetCompleteView.as_view(), name="password_reset_complete"),
]


# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']