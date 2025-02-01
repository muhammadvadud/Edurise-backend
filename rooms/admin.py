from django.contrib import admin
from .models import Rooms
from unfold.admin import ModelAdmin


admin.site.register(Rooms, ModelAdmin)
