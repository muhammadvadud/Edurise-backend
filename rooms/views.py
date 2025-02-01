from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView

from rooms.models import Rooms


class ListViewPage(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        context = {
            "rooms": Rooms.objects.filter(educenter=request.user.educenter)
            .order_by("id")
            .reverse()
        }
        return render(request, "room/list.html", context)


class CreateViewPage(LoginRequiredMixin, CreateView):
    template_name = "room/create.html"
    model = Rooms
    fields = [
        "name",
    ]

    # xonaga avtomatik educenter ni qo'shib qo'yish uchun
    def form_valid(self, form):
        form = form.save(commit=False)
        form.educenter = self.request.user.educenter
        form.save()
        messages.success(self.request, "Xona yaratildi")

        return redirect(reverse("rooms:list"))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("rooms:list"))


class DeleteViewPage(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "room/delete.html"
    model = Rooms
    success_url = reverse_lazy("rooms:list")

    def form_valid(self, form):
        messages.success(self.request, "Xona muvaffaqiyatli o'chirildi")
        return super().form_valid(form)

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(Rooms, id=id).educenter
            == self.request.user.educenter
        )


class EditViewPage(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "room/edit.html"
    model = Rooms
    fields = [
        "name",
    ]
    success_url = reverse_lazy("rooms:list")

    def form_valid(self, form):
        messages.success(self.request, "Xona muvaffaqiyatli o'zgartirildi")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("rooms:list"))

    def test_func(self):
        id = self.kwargs["pk"]
        return (
            get_object_or_404(Rooms, id=id).educenter
            == self.request.user.educenter
        )
