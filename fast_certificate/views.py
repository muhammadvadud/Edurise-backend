import json
from django.contrib import messages
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
import os
from django.views.generic import CreateView, DeleteView, UpdateView
from helpers.certificate import Certificate
from fast_certificate.models import FastCertificate as Cr
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from accounts.models import Users
from education.models import CertificateType


class ListViewPage(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        if request.user.educenter.certificate_boolen:
            eduid = request.user.educenter.id or request.user.educenter.parent_id

            fast_certificate = Cr.objects.filter(educenter_id=eduid).order_by("-id")

            context = {
                "fast_certificate": fast_certificate,
                "Users": Users,
            }
            return render(request, "fast_certificate/list.html", context)
        else:
            return render(request, "403.html", status=403)

    def post(self, request):
        name = request.POST.get("name")
        certificate_id = request.POST.get("certificate_id")

        if name == "delete":
            try:
                certificate = Cr.objects.get(id=certificate_id)
                certificate.delete()
                messages.success(request, "Certificate muvaffaqiyatli o'chirildi")
            except Cr.DoesNotExist:
                messages.error(request, "Certificate topilmadi")
        else:
            messages.error(request, "Certificate o'chirilmadi")

        return redirect("fast_certificate:list")


class CreateViewPage(LoginRequiredMixin, CreateView):
    template_name = "fast_certificate/create.html"
    model = Cr
    fields = ["first_name", "last_name", "course", "certificate_type"]

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        """Agar ruxsat bo'lmasa, 403 sahifasiga yo'naltirish"""
        if not request.user.educenter.certificate_boolen:
            return render(request, "403.html", status=403)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        eduid = self.request.user.educenter.id
        if eduid is None:
            eduid = self.request.user.educenter.parent

        data["form"].fields["certificate_type"].queryset = CertificateType.objects.filter(
            educenter=eduid
        )
        return data

    def form_valid(self, form):
        form.instance.educenter = self.request.user.educenter  # Avtomatik `educenter` qo'shish
        self.object = form.save()  # Formani saqlash

        # Sertifikat yaratish
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        course_name = form.cleaned_data["course"]
        ctype = get_object_or_404(CertificateType, id=form.cleaned_data["certificate_type"].id)

        c = Certificate(ctype.file)
        func = getattr(c, ctype.callback)

        # Sertifikatni yaratish
        filepath, filename = func(
            f"{last_name} {first_name}",
            course_name,
            "kursini muvaffaqiyatli yakunladi",
        )

        # Sertifikatni saqlash
        self.object.certificate.save(filename, open(filepath, "rb"))
        self.object.save()

        # Faylni vaqtincha o'chirish
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Error removing file: {e}")

        messages.success(self.request, "Sertifikat muvaffaqiyatli yaratildi")
        return redirect(reverse("fast_certificate:list"))

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags="danger")
        return redirect(reverse("fast_certificate:list"))
