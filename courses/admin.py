from django.contrib import admin
from .models import Courses
from unfold.admin import ModelAdmin


admin.site.register(Courses, ModelAdmin)
