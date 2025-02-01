from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import widgets
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from accounts.models import Users
from adm.forms import EduCenterUserCreateForm
from education.models import EduCenter
from middlewares.role import CheckRole


class ListViewPage(ListView):
    template_name = "education/list.html"
    model = EduCenter
    context_object_name = "educenters"

    def get_queryset(self):
        if CheckRole(
            self.request.user, roles=[Users.ROLE_SUPER_ADMIN, Users.ROLE_ADMIN]
        ):
            data = EduCenter.objects.all().order_by("id").reverse()
            return data
        else:
            data = (
                EduCenter.objects.filter(parent=self.request.user.educenter.id)
                .order_by("id")
                .reverse()
            )
            return data


class CreateViewPage(CreateView):
    template_name = "education/create.html"
    model = EduCenter
    fields = [
        "name",
    ]
    success_url = reverse_lazy("education:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["user_form"] = EduCenterUserCreateForm
        return data

    def form_valid(self, form):
        user_form = EduCenterUserCreateForm(self.request.POST)
        if user_form.is_valid():
            form = form.save(commit=False)
            form.parent = self.request.user.educenter.id
            form.save()

            try:
                user_form.instance.first_name = self.request.POST.get("name")
                user_form.instance.educenter_id = form.id
                user_form.instance.role = Users.ROLE_ADMINISTRATOR
                user_form.save()
            except:
                EduCenter.objects.get(id=form.id).delete()
            return redirect(reverse("education:list"))
        return render(
            self.request,
            "education/create.html",
            context={"user_form": user_form, "form": form},
        )


class DeleteViewPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "education/delete.html"
    model = EduCenter
    success_url = reverse_lazy("education:list")

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(EduCenter, id=id).parent
            == self.request.user.educenter.id
        )


class EditViewPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "education/edit.html"
    model = EduCenter
    fields = [
        "name",
    ]
    success_url = reverse_lazy("education:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["user_form"] = EduCenterUserCreateForm
        return data

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(EduCenter, id=id).parent
            == self.request.user.educenter.id
        )
