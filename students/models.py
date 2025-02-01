from django.db import models
from education.models import EduCenter


class Students(models.Model):
    MALE_GENDER = "Erkak"
    FEMALE_GENDER = "Ayol"

    ODD_DAYS = "Juft kunlar"
    EVEN_DAYS = "Toq kunlar"
    MATTER_DAYS = "Farqi yo'q"

    GENDERS = (
        (FEMALE_GENDER, FEMALE_GENDER),
        (MALE_GENDER, MALE_GENDER),
    )

    ACTIVE = "Aktiv"
    NOTACTIVE = "Aktiv emas"

    STATUS = ((ACTIVE, ACTIVE), (NOTACTIVE, NOTACTIVE))

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=100)
    photo = models.ImageField(
        upload_to="avatar/",
        default="avatar/default.jpg",
        null=True,
        blank=True,
    )

    gender = models.CharField(
        choices=GENDERS, max_length=50, default=MALE_GENDER
    )
    birth_day = models.DateField()
    educenter = models.ForeignKey(
        EduCenter, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.CharField(max_length=255, choices=STATUS, default=ACTIVE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
