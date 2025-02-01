from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import widgets
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    View,
    DeleteView,
    UpdateView,
)

from accounts.models import Users
from education.models import EduCenter
from .forms import EduCenterUserCreateForm


class ListViewPage(ListView):
    template_name = "adm/educenter/list.html"
    model = EduCenter
    context_object_name = "educenters"

    def get_queryset(self):
        data = EduCenter.objects.filter(parent=None).order_by("id").reverse()
        return data


class CreateViewPage(CreateView):
    template_name = "adm/educenter/create.html"
    model = EduCenter
    fields = [
        "name",
        "logo",
        "certificates"
    ]
    success_url = reverse_lazy("adm:edulist")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["user_form"] = EduCenterUserCreateForm
        return data

    def form_valid(self, form):
        educenter = form.save()
        user_form = EduCenterUserCreateForm(self.request.POST)
        if user_form.is_valid():
            user_form.instance.educenter = educenter
            user_form.instance.role = Users.ROLE_CEO
            user_form.save()
            return redirect(reverse("adm:edulist"))
        EduCenter.objects.filter(id=educenter).delete()
        return render(
            self.request,
            "adm/educenter/create.html",
            context={"user_form": user_form, "form": form},
        )


class DeleteViewPage(LoginRequiredMixin, DeleteView):
    template_name = "adm/educenter/delete.html"
    model = EduCenter
    success_url = reverse_lazy("adm:edulist")


class EditViewPage(LoginRequiredMixin, UpdateView):
    template_name = "adm/educenter/edit.html"
    model = EduCenter
    fields = [
        "name",
        "logo",
        "certificates"
    ]
    success_url = reverse_lazy("adm:edulist")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["user_form"] = EduCenterUserCreateForm
        return data


class EduLogin(View):

    def get(self, request, pk):
        user = Users.objects.filter(
            educenter_id=pk, role=Users.ROLE_CEO
        ).first()
        login(request, user)
        messages.success(request, "O'quv markazga kirildi")
        return redirect(reverse("home"))
