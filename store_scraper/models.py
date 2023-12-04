from django.db import models


class CoffeeStore(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="Name")
    address = models.CharField(max_length=2047, unique=True, verbose_name="Address")
    latitude = models.DecimalField(default=0.0, max_digits=20, decimal_places=15, verbose_name="Latitude")
    longitude = models.DecimalField(default=0.0, max_digits=20, decimal_places=15, verbose_name="Longitude")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "coffee_store"
        verbose_name = "Coffee Store"

    def __str__(self):
        return self.label
