from django.urls import path

from . import views

app_name = "corporate"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("thrivepoint-insights/", views.thrivepoint, name="thrivepoint"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
]
