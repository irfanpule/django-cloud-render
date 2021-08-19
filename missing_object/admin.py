from django.contrib import admin
from missing_object.models import MissingObject


@admin.register(MissingObject)
class MissingObjectAdmin(admin.ModelAdmin):
    search_fields = ('title',)
