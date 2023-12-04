from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from store_scraper.models import CoffeeStore
from store_scraper.serializers import CoffeeStoreSerializer
from store_scraper.tasks import scrape_zus_website


def index(request):
	context = {"title": "Store Scraper"}
	scrape_zus_website.delay()
	return render(request, "store_scraper/index.html", context)


class CoffeeStoreViewSet(ModelViewSet):
	queryset = CoffeeStore.objects.all()
	serializer_class = CoffeeStoreSerializer
	permission_classes = []
