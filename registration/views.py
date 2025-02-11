from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from courses.models import Courses
from registration.models import Registration


class ListViewPage(ListView):
    template_name = "registration/list.html"
    model = Registration
    context_object_name = "registration"

    def get_queryset(self):
        data = (
            Registration.objects.filter(educenter=self.request.user.educenter)
            .order_by("id")
            .reverse()
        )
        return data


class CreateViewPage(CreateView):
    template_name = "registration/create.html"
    model = Registration
    success_url = reverse_lazy("registration:list")
    fields = [
        "first_name",
        "last_name",
        "course",
        "phone",
        "days",
        "gender",
        "birth_day",
    ]

    def get_context_data(self, **kwargs):
        eduid = self.request.user.educenter.id
        if eduid is None:
            eduid = self.request.user.educenter.parent

        data = super().get_context_data(**kwargs)
        data["form"].fields["first_name"].label = "Ism"
        data["form"].fields["last_name"].label = "Familiya"
        data["form"].fields["course"].label = "Kurs"
        data["form"].fields["course"].queryset = Courses.objects.filter(
            educenter=eduid
        )
        data["form"].fields["phone"].label = "Telefon"
        data["form"].fields["days"].label = "Kunlar"
        data["form"].fields["gender"].label = "Jins"
        data["form"].fields["birth_day"].label = "Tug'ilgan_kun"
        # data['form'].fields['birth_day'].widget = widgets.TimeInput(attrs={"type": "date"})
        return data

    def form_valid(self, form):
        form = form.save(commit=False)
        form.educenter = self.request.user.educenter
        form.save()
        messages.success(self.request, "O'quvchi ro'yhatga olindi")
        return redirect(reverse("registration:list"))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("registration:list"))


class DeleteViewPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "registration/delete.html"
    model = Registration
    success_url = reverse_lazy("registration:list")
    context_object_name = "registration"

    def form_valid(self, form):
        messages.success(self.request, "O'quvchi o'chirildi")
        return super().form_valid(form)

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Registration, id=id).educenter
                == self.request.user.educenter
        )

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("registration:list"))


class EditViewPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "registration/edit.html"
    model = Registration
    fields = [
        "first_name",
        "last_name",
        "course",
        "phone",
        "days",
        "gender",
        "birth_day",
    ]

    success_url = reverse_lazy("registration:list")

    def form_valid(self, form):
        messages.success(self.request, "O'quvchi o'zgartirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("registration:list"))

    def test_func(self):
        id = self.kwargs["pk"]
        return (
                get_object_or_404(Registration, id=id).educenter
                == self.request.user.educenter
        )
