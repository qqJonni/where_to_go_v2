from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

from django.contrib import admin
from places.models import PlaceName, PlaceImage


class PicsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    readonly_fields = ["show_photo_preview"]

    def show_photo_preview(self, image):
        return image.show_photo_preview

    show_photo_preview.short_description = 'Photo Preview'
    show_photo_preview.allow_tags = True


@admin.register(PlaceName)
class PostAdmin(SortableAdminBase, admin.ModelAdmin):
    fields = ["title", "short_description", "long_description", "latitude", "longitude"]
    list_display = ['title']
    inlines = [PicsInline, ]


@admin.register(PlaceImage)
class PicAdmin(admin.ModelAdmin):
    ordering = ['sequence_number']
    raw_id_fields = ['place']
    readonly_fields = ["show_photo_preview"]

    def show_photo_preview(self, image):
        return image.show_photo_preview

    show_photo_preview.short_description = 'Photo Preview'
    show_photo_preview.allow_tags = True
