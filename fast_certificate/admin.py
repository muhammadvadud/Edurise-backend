from django.contrib import admin
from .models import FastCertificate
from unfold.admin import ModelAdmin


class AdminPageView(ModelAdmin):
    model = FastCertificate
    list_display = ["first_name", "course", "certificate", "id"]


admin.site.register(FastCertificate, AdminPageView)
