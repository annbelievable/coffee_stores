from django.shortcuts import render

# Create your views here.
def index(request):
    context = {"title": "Store Scraper"}
    return render(request, "store_scraper/index.html", context)