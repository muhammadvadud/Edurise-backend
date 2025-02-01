from django.contrib import admin
from .models import Groups
from unfold.admin import ModelAdmin


admin.site.register(Groups, ModelAdmin)
