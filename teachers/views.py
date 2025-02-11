from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import widgets
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from accounts.models import Users
from teachers.forms import (
    TeacherCreateWithUserForm,
    TeacherChangeWithUserForm,
    TeacherForm,
)
from teachers.models import Teachers


class ListViewPage(ListView):
    template_name = "teachers/list.html"
    model = Users
    context_object_name = "teachers"

    def get_queryset(self):
        data = (
            Users.objects.filter(
                educenter=self.request.user.educenter, role=Users.ROLE_TEACHER
            )
            .order_by("id")
            .reverse()
        )
        return data


class CreateViewPage(CreateView):
    template_name = "teachers/create.html"
    model = Users
    form_class = TeacherCreateWithUserForm

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["teacher_form"] = TeacherForm()
        # data['form'].fields['birth_day'].widget = widgets.TimeInput(attrs={"type": "date"})
        return data

    def form_valid(self, form):
        teacher_form = TeacherForm(self.request.POST)
        if teacher_form.is_valid():
            if int(self.request.POST["salary"]) > 100:
                messages.error(
                    self.request,
                    "Iltimos oylikni foizda kiriting (maksimal 100%)",
                    extra_tags="danger",
                )
                return redirect(reverse("teachers:list"))

            # User obyektini yaratish
            user = form.save(commit=False)
            user.educenter = self.request.user.educenter
            user.role = Users.ROLE_TEACHER

            # ⚠️ Bu joyda parolni hash’lamaymiz! Django avtomatik hash’laydi agar kerak bo‘lsa
            user.save()

            # Teacher obyektini yaratish
            teacher = teacher_form.save(commit=False)
            teacher.educenter = self.request.user.educenter
            teacher.user = user
            teacher.direction = self.request.POST["direction"]
            teacher.salary = self.request.POST["salary"]
            teacher.save()

            messages.success(self.request, "O'qituvchi qo'shildi")
        else:
            messages.error(self.request, teacher_form.errors, extra_tags="danger")

        return redirect(reverse("teachers:list"))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("teachers:list"))


class DeleteViewPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "teachers/delete.html"
    model = Users
    success_url = reverse_lazy("teachers:list")
    context_object_name = "teachers"

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Users, id=id).educenter
                == self.request.user.educenter
        )

    def form_valid(self, form):
        messages.success(self.request, "O'qituvchi o'chirildi")
        return super().form_valid(form)


class EditViewPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "teachers/edit.html"
    model = Users
    form_class = TeacherChangeWithUserForm

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["teacher_form"] = TeacherForm(
            initial=Teachers.objects.filter(
                user_id=self.kwargs["pk"]
            ).values()[0]
        )
        # data['form'].fields['birth_day'].widget = widgets.TimeInput(attrs={"type": "date"})
        return data

    def form_valid(self, form):
        if int(self.request.POST["salary"]) > 100:
            messages.error(
                self.request,
                "Iltimos oylikni foizda kiriting maxsimal 100",
                extra_tags="danger",
            )
            return redirect(self.request.META.get("HTTP_REFERER"))
        messages.success(self.request, "O'qituvchi o'zgartirildi")
        data = self.request.POST
        Teachers.objects.filter(user_id=self.kwargs["pk"]).update(
            salary=data["salary"], direction=data["direction"]
        )
        return super().form_valid(form)

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Users, id=id).educenter
                == self.request.user.educenter
        )

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(self.request.META.get("HTTP_REFERER"))
