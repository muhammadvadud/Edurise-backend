from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import widgets
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from accounts.models import Users
from courses.models import Courses
from helpers.Json import Json
from helpers.helpers import getDays, getMonthNumber, JournalCheck
from helpers.url import back
from payments.models import Payments
from registration.models import Registration
from rooms.models import Rooms
from students.models import Students
from .models import Groups, Journal
import datetime


class ListViewPage(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        user = self.request.user

        if user.role == Users.ROLE_TEACHER:
            groups = (
                Groups.objects.filter(
                    educenter=request.user.educenter, teacher=user.id
                )
                .order_by("id")
                .reverse()
            )
        else:
            groups = (
                Groups.objects.filter(educenter=request.user.educenter)
                .order_by("id")
                .reverse()
            )
        if request.GET.get("to") == "excel":
            json_data = {
                "Nomi": [group.name for group in groups],
                "Kurs": [group.course for group in groups],
                "O'qituvchi": [
                    f"{group.teacher.first_name} {group.teacher.last_name}"
                    for group in groups
                ],
                "Kunlar": [group.days for group in groups],
                "Xona": [group.room for group in groups],
                "Boshlangan kuni": [group.starting_day for group in groups],
                "Boshlanish vaqti": [group.starting_time for group in groups],
                "Narxi": [group.price for group in groups],
                "O'quvchilar": [group.users.count() for group in groups],
            }
            return Json.to_excel(json_data)

        context = {
            "groups": groups,
        }
        return render(request, "group/list.html", context)


class CreateViewPage(LoginRequiredMixin, CreateView):
    template_name = "group/create.html"
    model = Groups
    fields = [
        "name",
        "course",
        "teacher",
        "days",
        "room",
        "starting_time",
        "starting_day",
        "price",
    ]

    # qaysi filial Talabasi bo'lsa aynan shu filial o'qituvchilar va xonalarni filter qilib olish uchun
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        eduid = self.request.user.educenter.id
        if eduid is None:
            eduid = self.request.user.educenter.parent

        data["form"].fields["starting_time"].widget = widgets.TimeInput(
            attrs={"type": "time"}
        )
        # data["form"].fields['starting_day'].widget = widgets.DateTimeInput(attrs={"type": "date"})
        data["form"].fields["course"].queryset = Courses.objects.filter(
            educenter=eduid
        )
        data["form"].fields["teacher"].queryset = Users.objects.filter(
            role=Users.ROLE_TEACHER, educenter=self.request.user.educenter
        )
        data["form"].fields["room"].queryset = Rooms.objects.filter(
            educenter=self.request.user.educenter
        )
        return data

    # guruhga avtomatik educenter ni qo'shib qo'yish uchun
    def form_valid(self, form):
        form = form.save(commit=False)
        form.educenter = self.request.user.educenter
        form.save()
        messages.success(self.request, "Guruh muvaffaqiyatli yaratildi")
        return redirect(back(self.request))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(back(self.request))


class DeleteViewPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "group/delete.html"
    model = Groups

    def get_success_url(self):
        return reverse("groups:list")

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Groups, id=id).educenter
                == self.request.user.educenter
        )

    def form_valid(self, form):
        messages.success(self.request, "Guruh muvaffaqiyatli o'chirildi")
        return super().form_valid(form)


class EditViewPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "group/edit.html"
    model = Groups
    fields = [
        "name",
        "course",
        "teacher",
        "days",
        "room",
        "starting_time",
        "starting_day",
        "price",
    ]

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("groups:detail", kwargs={"pk": pk})

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Groups, id=id).educenter
                == self.request.user.educenter
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        eduid = self.request.user.educenter.id
        if eduid is None:
            eduid = self.request.user.educenter.parent

        data["form"].fields["course"].queryset = Courses.objects.filter(
            educenter=eduid
        )
        data["form"].fields["teacher"].queryset = Users.objects.filter(
            role=Users.ROLE_TEACHER, educenter=self.request.user.educenter
        )
        data["form"].fields["room"].queryset = Rooms.objects.filter(
            educenter=self.request.user.educenter
        )
        return data

    def form_valid(self, form):
        messages.success(self.request, "Guruh muvaffaqiyatli o'zgartirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(back(self.request))


class AddStudentViewPage(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request: HttpRequest, pk):
        group = get_object_or_404(Groups, id=pk)
        students = Registration.objects.filter(
            educenter=self.request.user.educenter, course=group.course
        )
        context = {
            "group": group,
            "students": students,
        }
        return render(request, "group/addStudent.html", context)

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Groups, id=id).educenter
                == self.request.user.educenter
        )

    def post(self, request, pk):
        data = self.request.POST
        group = Groups.objects.get(id=pk)

        u = Registration.objects.get(id=data["user"])

        user = Students.objects.create(
            first_name=u.first_name,
            last_name=u.last_name,
            status=Students.ACTIVE,
            educenter=self.request.user.educenter,
            phone=u.phone,
            gender=u.gender,
            birth_day=u.birth_day,
        )

        group.users.add(user)
        u.delete()
        return HttpResponse("OK")


class AddGroupStudent(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk):
        student = get_object_or_404(Students, id=pk)
        groups = Groups.objects.filter(educenter=self.request.user.educenter)

        context = {
            "groups": groups,
            "student": student,
        }
        return render(request, "group/addGroupStudent.html", context)

    def post(self, request, pk):
        data = self.request.POST
        student = get_object_or_404(Students, pk=pk)

        group = get_object_or_404(Groups, pk=data.get("group"))

        group.users.add(student)

        return HttpResponse("OK")


class RemoveStudentViewPage(View):

    def get(self, request, group, user):
        student = Students.objects.get(id=user)
        group = Groups.objects.get(id=group)

        context = {
            "student": student,
            "group": group,
        }

        return render(request, "group/removeStudent.html", context=context)

    def test_func(self):
        id = self.kwargs["group"]
        return (
                get_object_or_404(Groups, id=id).educenter
                == self.request.user.educenter
        )

    def post(self, request, group, user):
        g = Groups.objects.get(id=group)
        user = Students.objects.get(id=user)
        g.users.remove(user)
        messages.success(request, "Talaba guruhdan chiqarildi")
        return redirect(request.META.get("HTTP_REFERER"))


class StudentDebtViewPage(View):

    def get(self, request, group, user):
        student = Students.objects.get(id=user)
        group = Groups.objects.get(id=group)
        payments = Payments.objects.filter(
            group_id=group,
            student_id=student,
            educenter=request.user.educenter,
        )

        context = {
            "student": student,
            "payments": payments,
        }

        return render(request, "group/studentDebt.html", context=context)

    def test_func(self):
        id = self.kwargs["group"]
        return (
                get_object_or_404(Groups, id=id).educenter
                == self.request.user.educenter
        )

    def post(self, request, group, user):
        g = Groups.objects.get(id=group)
        user = Students.objects.get(id=user)
        g.users.remove(user)
        messages.success(request, "Talaba guruhdan chiqarildi")
        return redirect(request.META.get("HTTP_REFERER"))


class DetailPageView(View, UserPassesTestMixin):

    def get(self, request, pk):

        group = get_object_or_404(Groups, pk=pk)
        students = group.users.all()
        m = request.GET.get("month")
        # values_list("first_name", "last_name", "phone", "gender")
        # students = [list(obj) for obj in students]

        start_month = group.starting_day.month
        month_duration = group.course.month_duration + 1

        months = []

        i = start_month

        for month in range(start_month, start_month + month_duration):
            if i > 12:
                i = 1
            mm = datetime.datetime(group.starting_day.year, i, 1).strftime(
                "%b"
            )
            if mm in months:
                i = 1
                continue
            months.append(mm)
            i = i + 1

        date = datetime.datetime.now()
        if not m:
            if date.strftime("%b") in months:
                m = date.strftime("%b")
            else:
                m = months[0]

        # sday = group.starting_day
        month_number = getMonthNumber(m)
        days = getDays(date.year, month_number, group.days == Groups.ODD_DAYS)
        context = {
            "group": group,
            "students": students,
            "students_js": [
                {
                    "id": obj.id,
                    "last_name": obj.last_name,
                    "first_name": obj.first_name,
                }
                for obj in students
            ],
            "days": days,
            "month_name": m,
            "months": months,
            "m": m,
            "today": date,
            "month_number": month_number,
        }

        if (
                request.GET.get("to") == "excel"
                and request.GET.get("type") == "journal"
        ):
            FIO = [
                f"{obj['first_name']} {obj['last_name']}"
                for obj in students.values()
            ]
            sids = [str(obj["id"]) for obj in students.values()]
            json_data = {
                "F.I.O": FIO,
            }
            for day in days:
                json_data[f"{day} {m}"] = [
                    (
                        "-"
                        if JournalCheck(group.id, s, m, day) == ""
                           and day <= date.day
                        else "+"
                    )
                    for s in sids
                ]
            return Json.to_excel(json_data)
        elif (
                request.GET.get("to") == "excel"
                and request.GET.get("type") == "students"
        ):
            json_data = {
                "F.I.O": [
                    f"{student.first_name} {student.last_name}"
                    for student in students
                ],
                "Telefon": [str(student.phone) for student in students],
                "Tug'ulgan kuni": [
                    student.birth_day.strftime("%d.%m.%Y")
                    for student in students
                ],
                "Jinsi": [student.gender for student in students],
                "Status": [student.status for student in students],
                "Qo'shilgan": [
                    student.created_at.strftime("%d.%m.%Y")
                    for student in students
                ],
            }
            return Json.to_excel(json_data)

        return render(request, "group/detail.html", context=context)

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Groups, id=id).educenter
                == self.request.user.educenter
        )


class JournalPageView(LoginRequiredMixin, View):

    def post(self, request: HttpRequest):
        data = request.POST

        student = data.get("student")
        group = data.get("group")
        day = data.get("day")
        month = data.get("month")

        if not Journal.objects.filter(
                group_id=group, student_id=student
        ).exists():
            res = Journal.objects.create(
                group_id=group,
                student_id=student,
                data={},
                educenter=request.user.educenter,
            )
            if not res:
                return HttpResponse("ERROR")

        journal = Journal.objects.filter(group_id=group, student_id=student)
        data = journal.first()
        j = data.data
        status = "REMOVE"
        if month in j:
            days = j[month]
            if day in days:
                days.remove(day)
            else:
                status = "ADD"
                days.append(day)
            j[month] = days
        else:
            j[month] = [day]
            status = "ADD"

        journal.update(data=j)

        return HttpResponse(status)
