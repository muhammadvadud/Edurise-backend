import datetime

from django.db import models
from education.models import EduCenter
from accounts.models import Users
from groups.models import Groups
from students.models import Students


class Payments(models.Model):
    PAYME = "Payme"
    ClICK = "Click"
    NAQD = "Naqd"
    APELSIN = "Apelsin"
    PLASTIC_KARTA = "Plastic kartasi"
    BANK = "Bank hisobi"

    TYPE = (
        (APELSIN, APELSIN),
        (PLASTIC_KARTA, PLASTIC_KARTA),
        (BANK, BANK),
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
    chek = models.FileField(upload_to="chek/", default="chek/default.jpg")
    educenter = models.ForeignKey(EduCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.educenter.name
