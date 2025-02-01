from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import widgets
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from accounts.models import Users
from forms.user import StedentCreationCustomForm, StedentEditCustomForm
from groups.models import Groups
from students.models import Students


class ListViewPage(ListView):
    template_name = "students/list.html"
    model = Students
    context_object_name = "students"

    def get_queryset(self):
        user = self.request.user
        if self.request.user.role == Users.ROLE_TEACHER:
            groups = Groups.objects.filter(
                educenter=user.educenter, teacher=user.id
            )  # noqa
            data = [user for group in groups for user in group.users.all()]
        else:
            data = (
                Students.objects.filter(educenter=self.request.user.educenter)
                .order_by("id")
                .reverse()
            )
        return data


class CreateViewPage(CreateView):
    template_name = "students/create.html"
    model = Students
    form_class = StedentCreationCustomForm
    success_url = reverse_lazy("students:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # data['form'].fields['birth_day'].widget = widgets.TimeInput(attrs={"type": "date"})
        return data

    def form_valid(self, form):
        form = form.save(commit=False)
        form.educenter = self.request.user.educenter
        form.save()
        messages.success(self.request, "Talaba muvaffaqiyatli qo'shildi")
        return redirect(reverse("students:list"))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("students:list"))


class DeleteViewPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "students/delete.html"
    model = Students
    success_url = reverse_lazy("students:list")
    context_object_name = "student"

    def form_valid(self, form):
        messages.success(self.request, "Talaba muvaffaqiyatli o'chirildi")
        return super().form_valid(form)

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(Students, id=id).educenter
            == self.request.user.educenter
        )


class EditViewPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "students/edit.html"
    model = Students
    form_class = StedentEditCustomForm

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(Students, id=id).educenter
            == self.request.user.educenter
        )

    def form_valid(self, form):
        messages.success(self.request, "Talaba muvaffaqiyatli o'zgartirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("students:list"))
