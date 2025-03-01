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
from groups.models import Groups
from payments.models import Payments
from students.models import Students


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
        Payments.objects.create(
            student=student,
            group=group,
            type=data["type"],
            amount=data["amount"],
            date=data["date"],
            description=data["description"],
            educenter=self.request.user.educenter,
        )
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

        return data
