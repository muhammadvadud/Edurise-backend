from django.contrib import admin
from .models import Payments
from unfold.admin import ModelAdmin


admin.site.register(Payments, ModelAdmin)
