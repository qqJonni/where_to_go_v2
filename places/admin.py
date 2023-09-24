from django.contrib import admin
from places.models import PlaceName, PlaceImage
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin
from adminsortable.utils import get_is_sortable


class PicsInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    readonly_fields = ["photo_preview"]

    def queryset(self, request):
        qs = super(PicsInline, self).queryset(request).filter(
            numb__icontains='foo')
        if get_is_sortable(qs):
            self.model.is_sortable = True
        else:
            self.model.is_sortable = False
        return qs

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = 'Photo Preview'
    photo_preview.allow_tags = True


@admin.register(PlaceName)
class PostAdmin(SortableAdminBase, admin.ModelAdmin):
    fields = ["title", "short_description", "long_description", "latitude", "longitude", "slug"]
    list_display = ['title']
    inlines = [PicsInline, ]


@admin.register(PlaceImage)
class PicAdmin(admin.ModelAdmin):
    list_display = ['numb', "place", "photo_preview"]
    ordering = ['numb', ]
    readonly_fields = ["photo_preview"]

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = 'Photo Preview'
    photo_preview.allow_tags = True
