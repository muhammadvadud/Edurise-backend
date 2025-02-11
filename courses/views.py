from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views import View

from accounts.models import Users
from .models import Courses
from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from .mixins import CeoRequiredMixin


class ListViewPage(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        # Foydalanuvchining ishlaydigan `EduCenter` ID sini olish
        eduid = request.user.educenter.id or request.user.educenter.parent_id

        # Shu `EduCenter` ga tegishli kurslarni olish
        context = {
            "courses": Courses.objects.filter(educenter_id=eduid).order_by("-id"),
            "Users": Users,
        }
        return render(request, "course/list.html", context)


class CreateViewPage(LoginRequiredMixin, CeoRequiredMixin, CreateView):
    template_name = "course/create.html"
    model = Courses
    fields = [
        "name",
        "duration",
        "month_duration",
        "description",
    ]

    # guruhga avtomatik educenter ni qo'shib qo'yish uchun
    def form_valid(self, form):
        month = self.request.POST.get("month_duration")

        if int(month) > 12:
            messages.success(
                self.request,
                "Kurs 12 oydan ko'p bo'lishi mumkun emas",
                extra_tags="danger",
            )
            return redirect(reverse("courses:list"))

        form = form.save(commit=False)
        form.educenter = self.request.user.educenter
        form.save()
        messages.success(self.request, "Kurs muvaffaqiyatli yaratildi")
        return redirect(reverse("courses:list"))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("courses:list"))


class DeleteViewPage(
    LoginRequiredMixin, UserPassesTestMixin, CeoRequiredMixin, DeleteView
):
    template_name = "course/delete.html"
    model = Courses
    success_url = reverse_lazy("courses:list")

    def form_valid(self, form):
        messages.success(self.request, "Kurst muvaffaqiyatli o'chirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("courses:list"))

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Courses, id=id).educenter
                == self.request.user.educenter
        )


class EditViewPage(LoginRequiredMixin, CeoRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "course/edit.html"
    model = Courses
    fields = [
        "name",
        "duration",
        "month_duration",
        "description",
    ]
    success_url = reverse_lazy("courses:list")

    def form_valid(self, form):
        month = self.request.POST.get("month_duration")

        if int(month) > 12:
            messages.success(
                self.request,
                "Kurs 12 oydan ko'p bo'lishi mumkun emas",
                extra_tags="danger",
            )
            return redirect(reverse("courses:list"))

        messages.success(self.request, "Kurst muvaffaqiyatli o'zgartirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("courses:list"))

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Courses, id=id).educenter
                == self.request.user.educenter
        )
