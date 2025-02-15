from unfold.admin import ModelAdmin

from django.contrib import admin
from certificate.models import Certificate


# Register your models here.
class AdminPageView(ModelAdmin):
    model = Certificate
    list_display = ["student", "course", "certificate", "id"]


admin.site.register(Certificate, AdminPageView)
