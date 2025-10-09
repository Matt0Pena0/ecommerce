from django.urls import path

from .views import home_view, contact_view


app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("Contact/", contact_view, name="contact"),
]
