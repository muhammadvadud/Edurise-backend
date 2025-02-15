from django.db import models
from courses.models import Courses
from students.models import Students
import os


class Certificate(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    certificate = models.FileField(upload_to="certificates/")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        """Certificate faylini o‘chirish"""
        if self.certificate:
            if os.path.isfile(self.certificate.path):
                os.remove(self.certificate.path)
        super().delete(*args, **kwargs)
