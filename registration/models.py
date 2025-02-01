from django.db import models

from courses.models import Courses
from education.models import EduCenter


class Registration(models.Model):
    MALE_GENDER = "Erkak"
    FEMALE_GENDER = "Ayol"

    ODD_DAYS = "Juft kunlar"
    EVEN_DAYS = "Toq kunlar"
    MATTER_DAYS = "Farqi yo'q"

    GENDERS = (
        (FEMALE_GENDER, FEMALE_GENDER),
        (MALE_GENDER, MALE_GENDER),
    )

    DAYS = (
        (MATTER_DAYS, MATTER_DAYS),
        (ODD_DAYS, ODD_DAYS),
        (EVEN_DAYS, EVEN_DAYS),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=100)
    days = models.CharField(max_length=255, choices=DAYS, default=MATTER_DAYS)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    gender = models.CharField(
        choices=GENDERS, max_length=50, default=MALE_GENDER
    )
    birth_day = models.DateField(blank=True, null=True)
    educenter = models.ForeignKey(
        EduCenter, on_delete=models.CASCADE, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
