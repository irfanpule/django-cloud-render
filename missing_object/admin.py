from django.contrib import admin
from missing_object.models import MissingObject, ImageObject


class ImageInline(admin.TabularInline):
    model = ImageObject
    extra = 10


@admin.register(MissingObject)
class MissingObjectAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ('title',)
