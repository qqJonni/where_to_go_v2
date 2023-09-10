from django.contrib import admin
from places.models import PlaceName


@admin.register(PlaceName)
class PlaceNameAdmin(admin.ModelAdmin):
    pass


