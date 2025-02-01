from django.db import models
from education.models import EduCenter


class Courses(models.Model):
    DURATION = (
        (30, 30),
        (40, 40),
        (60, 60),
        (90, 90),
        (120, 120),
        (180, 180),
        (240, 240),
        (280, 280),
        (300, 300),
    )

    name = models.CharField(max_length=255)
    duration = models.IntegerField(choices=DURATION, default=90)
    educenter = models.ForeignKey(EduCenter, on_delete=models.CASCADE)
    month_duration = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
