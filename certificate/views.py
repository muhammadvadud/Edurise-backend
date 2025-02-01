import json

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views import View
import os

from groups.models import Groups
from helpers.certificate import Certificate
from students.models import Students
from certificate.models import Certificate as Cr
from education.models import CertificateType


class GenerateCertificatePageView(View):

    def get(self, request, group):
        group = Groups.objects.get(id=group)
        students = group.users.all()
        certificates = request.user.educenter.certificates.all()

        context = {"group": group, "students": students, "certificates": certificates}

        return render(request, "certificate/generate.html", context)

    def post(self, request: HttpRequest, group):
        group = Groups.objects.get(id=group)

        student = get_object_or_404(Students, id=request.POST.get("student"))
        ctype = get_object_or_404(CertificateType, id=request.POST.get("certificate_type"))

        c = Certificate(ctype.file)
        func = getattr(c, ctype.callback)

        filepath, filename = func(
            f"{student.last_name} {student.first_name}",
            group.course.name,
            "kursini muvaffaqiyatli yakunladi",
        )

        certificate = Cr()
        certificate.course = group.course
        certificate.student = student
        certificate.certificate.save(filename, open(filepath, "rb"))
        certificate.save()
        url = "https://edusystem.uz{}".format(certificate.certificate.url)

        try:
            os.remove(filepath)
        except:
            pass

        return HttpResponse(
            json.dumps({"url": url, "success": True}),
            content_type="application/json",
        )
