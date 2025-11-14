from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'country', 'price_per_night', 'is_available']
    list_filter = ['city', 'country', 'property_type', 'is_available']
    search_fields = ['title', 'city', 'country']