from django.contrib import admin
from .models import Dataset

# admin.site.register(Dataset)

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')

