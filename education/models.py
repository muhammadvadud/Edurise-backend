from django.db import models
from django.utils.translation import gettext_lazy as _


class CertificateType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    file = models.ImageField(upload_to="certificates/", verbose_name=_("Fayil"))
    callback = models.CharField(max_length=255, verbose_name=_("Funcsiya"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Sertifikat")
        verbose_name_plural = _("Sertifikat turlari")


class EduCenter(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logo/", default="logo/default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.BigIntegerField(blank=True, null=True)
    certificates = models.ManyToManyField("CertificateType", verbose_name=_("Sertifikatlar"))

    def __str__(self):
        return self.name
