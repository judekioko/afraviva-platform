from django.urls import path

from . import views

app_name = "farms_hub"

urlpatterns = [
    path("", views.update_list, name="list"),
    path("<slug:slug>/", views.update_detail, name="detail"),
]
