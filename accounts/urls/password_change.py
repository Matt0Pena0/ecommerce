from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path

from accounts.views import BasePasswordChangeView


urlpatterns = [
    path("", BasePasswordChangeView.as_view(), name="change"),
    path(
        "complete/",
        PasswordChangeDoneView.as_view(
            template_name="accounts/password_change/Complete.html"
        ),
        name="complete",
    ),
]
