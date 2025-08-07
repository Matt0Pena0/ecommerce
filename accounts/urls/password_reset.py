from django.urls import path

from accounts.views import (BasePasswordResetCompleteView,
                            BasePasswordResetConfirmView,
                            BasePasswordResetDoneView, BasePasswordResetView)


urlpatterns = [
    path("", BasePasswordResetView.as_view(), name="reset"),
    path(
        "done/",
        BasePasswordResetDoneView.as_view(),
        name="done",
    ),
    path(
        "confirm/<uidb64>/<token>/",
        BasePasswordResetConfirmView.as_view(),
        name="confirm",
    ),
    path(
        "complete/",
        BasePasswordResetCompleteView.as_view(),
        name="complete",
    ),
]
