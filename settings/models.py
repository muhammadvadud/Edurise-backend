from django.db import models
from education.models import EduCenter


class Settings(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()
    educenter = models.ForeignKey(EduCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.key
