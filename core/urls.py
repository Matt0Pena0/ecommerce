from django.urls import path

from .views import home_view


app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    # path("contact/ccbv", ContactView.as_view(), name="contact"),
]
