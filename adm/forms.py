from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import Users
from django import forms


class UserCreationCustomForm(UserCreationForm):
    class Meta:
        model = Users
        fields = [
            "first_name",
            "last_name",
            "username",
            "phone",
            "gender",
            "birth_day",
            "role",
            "photo",
        ]


class UserChangeCustomForm(UserChangeForm):
    password = None

    class Meta:
        model = Users
        fields = [
            "first_name",
            "last_name",
            "phone",
            "gender",
            "birth_day",
            "role",
            "photo",
        ]


class EduCenterUserCreateForm(UserCreationForm):
    class Meta:
        model = Users
        fields = [
            "username",
            "first_name",
            "last_name",
        ]
        labels = {
            "username": "Foydalanuvchi nomi",
            "first_name": "Foydalanuvchi ismi",
            "last_name": "Foydalanuvchi familyasi",
        }
