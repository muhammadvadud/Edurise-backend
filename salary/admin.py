from django.contrib import admin
from salary.models import TeacherSalary
from unfold.admin import ModelAdmin

admin.site.register(TeacherSalary, ModelAdmin)
