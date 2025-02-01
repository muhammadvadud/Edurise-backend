from django.contrib import admin

from teachers.models import Teachers
from unfold.admin import ModelAdmin


admin.site.register(Teachers, ModelAdmin)
