from django.db import models
from education.models import EduCenter


class Rooms(models.Model):
    name = models.CharField(max_length=255)
    educenter = models.ForeignKey(EduCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
