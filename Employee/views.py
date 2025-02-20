from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Users
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from adm.forms import UserCreationCustomForm, UserChangeCustomForm
from helpers.url import back


class ListPageView(LoginRequiredMixin, ListView):
    template_name = "Employee/list.html"
    model = Users

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["object_list"] = Users.objects.filter(
            ~Q(role=Users.ROLE_CEO),
            ~Q(role=Users.ROLE_ADMINISTRATOR),
            educenter=self.request.user.educenter,
        )
        return data


class CreatePageView(LoginRequiredMixin, CreateView):
    template_name = "Employee/create.html"
    model = Users
    form_class = UserCreationCustomForm

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["form"].fields["role"].choices = [
            (Users.ROLE_MANGER, "Manijer"),
            (Users.ROLE_CASHER, "Kasir"),
        ]
        return data

    def form_valid(self, form):
        form.save(commit=False)
        form.instance.educenter = self.request.user.educenter
        form.save()
        messages.success(self.request, "Xodim qo'shildi")
        return redirect(back(self.request))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(self.request.META.get("HTTP_REFERER"))


class EditPageView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Users
    template_name = "Employee/edit.html"
    form_class = UserChangeCustomForm

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(*args, **kwargs)
        data["form"].fields["role"].choices = [
            (Users.ROLE_MANGER, "Manijer"),
            (Users.ROLE_CASHER, "Kasir"),
        ]
        return data

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(Users, id=id).educenter
            == self.request.user.educenter
        )

    def form_valid(self, form):
        messages.success(self.request, "Xodim o'zgartirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(self.request.META.get("HTTP_REFERER"))

    def get_success_url(self):
        return back(self.request)


class DeletePageView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Users
    template_name = "Employee/delete.html"

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(Users, id=id).educenter
            == self.request.user.educenter
        )

    def get_success_url(self):
        return back(self.request)

    def form_valid(self, form):
        messages.success(self.request, "Xodim o'chirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(self.request.META.get("HTTP_REFERER"))
