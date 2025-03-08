from django.db import models
from django.utils.translation import gettext_lazy as _


class CertificateType(models.Model):
    educenter_name = models.CharField(max_length=255, verbose_name=_("O'quv markaz nomi"))
    name = models.CharField(max_length=255, verbose_name=_("Nomi"))
    file = models.ImageField(upload_to="certificates/", verbose_name=_("Fayil"))
    callback = models.CharField(max_length=255, verbose_name=_("Funksiya"))

    def __str__(self) -> str:
        return self.educenter_name

    class Meta:
        verbose_name = _("Sertifikat")
        verbose_name_plural = _("Sertifikat turlari")


class EduCenter(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="logo/", default="logo/default.jpg", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.BigIntegerField(blank=True, null=True)
    certificates = models.ManyToManyField("CertificateType", null=True, blank=True, verbose_name=_("Sertifikatlar"))
    certificate_boolen = models.BooleanField(default=False, verbose_name=_("Sertifikat mumkim yoki mumkin emas?"))

    def __str__(self):
        return self.name
