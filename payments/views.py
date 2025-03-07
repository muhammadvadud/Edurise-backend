from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.forms import widgets
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from courses.models import Courses
from groups.models import Groups
from payments.models import Payments
from students.models import Students
from django.contrib import messages
from helpers.chek import generate_receipt
from django.conf import settings


class ListViewPage(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        # Foydalanuvchi sanalarni tanlamagan bo'lsa, filter qo'llanmasin
        payments = Payments.objects.filter(educenter=request.user.educenter).order_by("-id")

        if start_date and end_date:
            payments = payments.filter(date__gte=start_date, date__lte=end_date)

        total_payment = payments.aggregate(Sum("amount"))

        context = {
            "payments": payments,
            "total_payment": total_payment,
            "start_date": start_date,  # Template-da tekshirish uchun kerak
            "end_date": end_date,
        }
        return render(request, "payments/list.html", context)


class PaymentViewPage(View):
    def post(self, request):
        data = self.request.POST
        group = Groups.objects.get(pk=data["group_id"])
        student = Students.objects.get(pk=data["student_id"])

        # Avval Payment modeliga saqlash
        payment = Payments.objects.create(
            student=student,
            group=group,
            type=data["type"],
            amount=data["amount"],
            date=data["date"],
            description=data["description"],
            educenter=request.user.educenter
        )

        # Modeldan ma'lumot olib, chek yaratish
        receipt_path = generate_receipt(
            student_name=f"{student.first_name} {student.last_name}",
            group_name=group.name,
            payment_type=payment.type,
            amount=payment.amount,
            educenter_name=payment.educenter.name,
            date=payment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            course_name=group.course.name,
            payment_id=payment.id,
            status="Muvaffaqiyatli",
        )

        # Hosil bo'lgan chekni modelga qayta yozish
        payment.chek = receipt_path.replace(str(settings.MEDIA_ROOT) + "/", "")
        payment.save(update_fields=["chek"])

        messages.success(self.request, "To'lov muvaffaqiyatli amalga oshdi")
        return redirect("groups:detail", pk=group.id)


class PayViewPage(LoginRequiredMixin, CreateView):
    template_name = "payments/pay.html"
    model = Payments

    fields = [
        "student",
        "group",
        "type",
        "amount",
        "date",
        "description",
    ]
    success_url = reverse_lazy("groups:list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        group = Groups.objects.filter(
            educenter=self.request.user.educenter, pk=self.kwargs["group"]
        )
        students = Students.objects.filter(
            educenter=self.request.user.educenter, pk=self.kwargs["student"]
        )

        data["form"].fields["student"].queryset = students
        data["form"].fields["student"].widget = widgets.TextInput(
            attrs={
                "type": "text",
                "value": f"{students.first().first_name} {students.first().last_name}",
                "readonly": True,
            }
        )
        data["form"].fields["student_id"] = forms.CharField(
            widget=widgets.TextInput(
                attrs={
                    "type": "hidden",
                    "value": students.first().id,
                    "readonly": True,
                }
            )
        )

        data["form"].fields["group"].queryset = group
        data["form"].fields["group"].widget = widgets.TextInput(
            attrs={
                "type": "text",
                "value": group.first().name,
                "readonly": True,
            }
        )
        data["form"].fields["group_id"] = forms.CharField(
            widget=widgets.TextInput(
                attrs={
                    "type": "hidden",
                    "value": group.first().id,
                    "readonly": True,
                }
            )
        )

        data["form"].fields["date"].widget = widgets.DateTimeInput(
            attrs={"type": "date"}
        )
        data["form"].fields["amount"].widget = widgets.TextInput(
            attrs={"id": "amountInput", "type": "text"}
        )

        return data
