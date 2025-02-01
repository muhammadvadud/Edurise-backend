from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from courses.models import Courses
from groups.models import Groups
from registration.models import Registration
from rooms.models import Rooms
from students.models import Students
from teachers.models import Teachers


class Dashboard(LoginRequiredMixin, generic.TemplateView):

    def get(self, request: HttpRequest):
        context = {
            "students": Students.objects.filter(
                educenter=self.request.user.educenter
            ).count(),
            "lids": Registration.objects.filter(
                educenter=self.request.user.educenter
            ).count(),
            "teachers": Teachers.objects.filter(
                educenter=self.request.user.educenter
            ).count(),
            "groups": Groups.objects.filter(
                educenter=self.request.user.educenter
            ).count(),
            "rooms": Rooms.objects.filter(
                educenter=self.request.user.educenter
            ).count(),
            "courses": Courses.objects.filter(
                educenter=self.request.user.educenter
            ).count(),
        }
        return render(request, "dashboard.html", context)
