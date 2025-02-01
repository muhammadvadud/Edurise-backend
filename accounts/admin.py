from django.contrib import admin
from .models import Users
from unfold.admin import ModelAdmin


class AdminPageView(ModelAdmin):
    model = Users
    list_display = ["id", "first_name", "last_name", "gender"]


admin.site.register(Users, AdminPageView)
