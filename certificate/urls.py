from django.urls import path
from .views import GenerateCertificatePageView, delete_certificate

app_name = "certificate"

urlpatterns = [
    path(
        "generate/<int:group>/",
        GenerateCertificatePageView.as_view(),
        name="generate",
    ),
    path(
        "delete/<int:certificate_id>/",
        delete_certificate,
        name="delete",
    )

]
