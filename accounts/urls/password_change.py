from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path

from accounts.views import BasePasswordChangeView

urlpatterns = [
    path("", BasePasswordChangeView.as_view(), name="change"),
    path(
        "done/",
        PasswordChangeDoneView.as_view(
            template_name="accounts/password_change/done.html"
        ),
        name="done",
    ),
]
