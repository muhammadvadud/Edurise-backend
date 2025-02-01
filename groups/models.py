from django.db import models

from accounts.models import Users
from courses.models import Courses
from education.models import EduCenter
from rooms.models import Rooms
from students.models import Students


class Groups(models.Model):
    ODD_DAYS = "Toq kunlar"
    EVEN_DAYS = "Juft kunlar"

    DAYS = ((ODD_DAYS, ODD_DAYS), (EVEN_DAYS, EVEN_DAYS))

    name = models.CharField(max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Users, on_delete=models.CASCADE, related_name="group_teacher"
    )
    days = models.CharField(max_length=255, choices=DAYS)
    room = models.ForeignKey(
        Rooms, on_delete=models.CASCADE, related_name="group_room"
    )
    starting_time = models.TimeField()
    starting_day = models.DateField()
    educenter = models.ForeignKey(
        EduCenter, on_delete=models.CASCADE, related_name="group_education"
    )
    price = models.CharField(max_length=255)
    users = models.ManyToManyField(
        Students, blank=True, null=True, related_name="groups"
    )

    def __str__(self):
        return self.name


class Journal(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    data = models.JSONField()
    educenter = models.ForeignKey(
        EduCenter, on_delete=models.CASCADE, related_name="group_journal"
    )

    def __str__(self):
        return f"{self.group.name} | {self.student.first_name}"
