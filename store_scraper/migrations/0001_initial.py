# Generated by Django 4.2.7 on 2023-12-03 14:09

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CoffeeStore",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(db_index=True, max_length=255, unique=True, verbose_name="Name")),
                ("address", models.CharField(max_length=2047, unique=True, verbose_name="Address")),
                (
                    "latitude",
                    models.DecimalField(decimal_places=15, default=0.0, max_digits=20, verbose_name="Latitude"),
                ),
                (
                    "longitude",
                    models.DecimalField(decimal_places=15, default=0.0, max_digits=20, verbose_name="Longitude"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Updated at")),
            ],
            options={
                "verbose_name": "Coffee Store",
                "db_table": "coffee_store",
            },
        ),
    ]
