import datetime

from django.db import models
from education.models import EduCenter
from accounts.models import Users
from groups.models import Groups
from students.models import Students
from django.conf import settings

import os


class Payments(models.Model):
    PAYME = "Payme"
    ClICK = "Click"
    NAQD = "Naqd"
    PLASTIC_KARTA = "Plastic kartasi"

    TYPE = (
        (PLASTIC_KARTA, PLASTIC_KARTA),
        (NAQD, NAQD),
        (PAYME, PAYME),
        (ClICK, ClICK),
    )

    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    group = models.ForeignKey(
        Groups, on_delete=models.CASCADE, related_name="payment_groups"
    )
    type = models.CharField(max_length=255, choices=TYPE)
    amount = models.BigIntegerField()
    date = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True, null=True)
    chek = models.FileField(upload_to="chek/", default="chek/chek.jpg")
    educenter = models.ForeignKey(EduCenter, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        """Agar to'lov o‘chirib yuborilsa, fayl ham o‘chsin"""
        if self.chek and self.chek.name != "chek/default.jpg":
            chek_path = os.path.join(settings.MEDIA_ROOT, self.chek.name)
            if os.path.exists(chek_path):
                os.remove(chek_path)  # Faylni o‘chirish
        super().delete(*args, **kwargs)  # Asl delete funksiyasini chaqiramiz

    def __str__(self):
        return self.educenter.name
