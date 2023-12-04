from rest_framework.serializers import HyperlinkedModelSerializer

from store_scraper.models import CoffeeStore


class CoffeeStoreSerializer(HyperlinkedModelSerializer):
	class Meta:
		model = CoffeeStore
		fields = ["name", "address", "latitude", "longitude"]
