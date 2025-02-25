from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path("", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    path("adm/", include("adm.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("courses/", include("courses.urls")),
    path("education/", include("education.urls")),
    path("groups/", include("groups.urls")),
    path("payments/", include("payments.urls")),
    path("rooms/", include("rooms.urls")),
    path("settings/", include("settings.urls")),
    path("students/", include("students.urls")),
    path("teachers/", include("teachers.urls")),
    path("registration/", include("registration.urls")),
    path("certificate/", include("certificate.urls")),
    path("employee/", include("Employee.urls")),
    path("api/", include("api.urls")),
    path("fast-certificate/", include("fast_certificate.urls")),
    re_path(r"media/(.*)", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"static/(.*)", serve, {"document_root": settings.STATIC_ROOT}),
]
