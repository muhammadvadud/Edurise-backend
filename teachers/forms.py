from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from accounts.models import Users
from teachers.models import Teachers


class TeacherCreateWithUserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = [
            "first_name",
            "last_name",
            "username",
            "phone",
            "gender",
            "birth_day",
            "status",
            "photo",
        ]


class TeacherChangeWithUserForm(UserChangeForm):
    password = None

    class Meta:
        model = Users
        fields = [
            "first_name",
            "last_name",
            "username",
            "phone",
            "gender",
            "birth_day",
            "status",
            "photo",
        ]


class TeacherForm(forms.ModelForm):
    salary = forms.IntegerField(label="Ish haqi (foizda)")
    direction = forms.CharField(label="Yonalishi")

    class Meta:
        model = Teachers
        fields = []
