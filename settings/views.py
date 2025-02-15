from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from education.models import EduCenter
from settings.forms import EduCenterEditForm


class ListViewPage(View):

    def get(self, request):
        context = {
            "data": EduCenter.objects.filter(
                id=request.user.educenter.id
            ).first()
        }

        return render(request, "settings/list.html", context)


class EditViewPage(View):

    def get(self, request):
        educenter = EduCenter.objects.get(id=request.user.educenter.id)

        context = {
            "form": EduCenterEditForm(
                initial={
                    "name": educenter.name,
                    "parent": educenter.parent,
                }
            )
        }

        return render(request, "settings/edit.html", context)

    def post(self, request):

        instance = EduCenter.objects.get(id=request.user.educenter.id)

        form = EduCenterEditForm(
            request.POST, request.FILES, instance=instance
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Sozlamalar o'zgartirildi")
        else:
            messages.error(request, form.errors, extra_tags="danger")

        return redirect(reverse("settings:list"))
