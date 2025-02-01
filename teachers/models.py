from django.db import models

from accounts.models import Users
from education.models import EduCenter


class Teachers(models.Model):
    salary = models.CharField(max_length=255, blank=True, null=True)
    direction = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    educenter = models.ForeignKey(EduCenter, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name
