from django.contrib import admin
from .models import Settings
from unfold.admin import ModelAdmin


admin.site.register(Settings, ModelAdmin)
