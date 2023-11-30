from django.urls import path

from . import views

app_name = "store_scraper"

urlpatterns = [
    path("", views.index, name="index"),
]
