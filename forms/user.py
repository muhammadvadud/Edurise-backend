from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from students.models import Students


class StedentCreationCustomForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            "first_name",
            "last_name",
            "phone",
            "gender",
            "birth_day",
            "status",
        ]


class StedentEditCustomForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            "first_name",
            "last_name",
            "phone",
            "gender",
            "birth_day",
        ]
