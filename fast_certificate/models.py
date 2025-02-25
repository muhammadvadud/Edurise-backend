from django.db import models
from education.models import EduCenter, CertificateType
import os


class FastCertificate(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    course = models.CharField(max_length=120)
    certificate = models.FileField(upload_to="certificates/")
    educenter = models.ForeignKey(EduCenter, on_delete=models.CASCADE)
    certificate_type = models.ForeignKey("education.CertificateType", on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        """Certificate faylini o‘chirish"""
        if self.certificate:
            if os.path.isfile(self.certificate.path):
                os.remove(self.certificate.path)
        super().delete(*args, **kwargs)
