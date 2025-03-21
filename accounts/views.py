from datetime import datetime

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from pandas.core.groupby.indexing import GroupByPositionalSelector

from accounts.models import Users
from certificate.models import Certificate
from groups.models import Groups
from payments.models import Payments
from students.models import Students
from teachers.models import Teachers


class ProfilePageView(View):

    def get(self, request, pk):
        user = get_object_or_404(Students, id=pk)

        if user.educenter != request.user.educenter:
            raise Http404

        groups = user.groups.all()
        certificates = Certificate.objects.filter(student_id=pk)
        payments = Payments.objects.filter(student_id=pk)

        context = {
            "udata": user,
            "groups": groups,
            "certificates": certificates,
            "payments": payments,
        }
        return render(request, "registration/profile.html", context=context)


class TeacherProfilePageView(View):
    def get(self, request, pk):
        user = get_object_or_404(Users, id=pk)

        # User roli va educenterni tekshirish
        # if user.role != Users.ROLE_TEACHER:
        #     raise Http404("Foydalanuvchi o'qituvchi emas")
        #
        # if user.educenter != request.user.educenter:
        #     raise Http404("Bu o'qituvchi sizning edukatsiya markaziga tegishli emas")

        # Guruhlar va o'qituvchi ma'lumotlarini olish
        groups = Groups.objects.filter(teacher=user)
        teacher = get_object_or_404(Teachers, user=user)

        today = datetime.today()
        salary_total = 0

        # Maoshni hisoblash
        for group in groups:
            payments = Payments.objects.filter(group=group, date__month=today.month)
            for payment in payments:
                salary_total += payment.amount

        # Maoshni hisoblash: maoshni summasi + o'qituvchining maoshi
        salary = (salary_total // 100) * int(teacher.salary) if teacher.salary else 0

        context = {
            "udata": user,
            "groups": groups,
            "teacher_data": teacher,
            "salary": salary,
            "salary_total": salary_total,
        }

        return render(request, "registration/teacher_profile.html", context=context)
