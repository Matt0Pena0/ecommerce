from django.urls import path

from accounts.views import CustomLoginView


app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    # path("register/", register, name="register"),
]