from django.urls import path

from . import views

app_name = "store_scraper"

urlpatterns = [
    path("scrape/", views.index, name="index"),
	path("api/coffee-stores/", views.CoffeeStoreViewSet.as_view({"get": "list"}), name="coffee_stores_api"),
]
