from django.contrib import admin
from .models import EduCenter, CertificateType
from unfold.admin import ModelAdmin


admin.site.register(EduCenter, ModelAdmin)
admin.site.register(CertificateType, ModelAdmin)
