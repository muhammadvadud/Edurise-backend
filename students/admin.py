from django.contrib import admin
from .models import Students
from unfold.admin import ModelAdmin


admin.site.register(Students, ModelAdmin)
