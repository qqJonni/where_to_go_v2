from django.contrib import admin
from places.models import PlaceName, PlaceImage


@admin.register(PlaceName)
class PostAdmin(admin.ModelAdmin):
    fields = ["title", "short_description", "long_description", "longitude", "latitude"]
    list_display = ['pk', 'title']


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    raw_id_fields = ['place']
    list_display = ['numb', 'place']

