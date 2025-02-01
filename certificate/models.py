from django.db import models

from courses.models import Courses
from students.models import Students


class Certificate(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    certificate = models.FileField(upload_to="certificates/")
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
