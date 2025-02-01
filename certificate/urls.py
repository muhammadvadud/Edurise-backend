from django.urls import path
from .views import GenerateCertificatePageView

app_name = "certificate"

urlpatterns = [
    path(
        "generate/<int:group>/",
        GenerateCertificatePageView.as_view(),
        name="generate",
    )
]
