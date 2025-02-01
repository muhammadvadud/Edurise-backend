from django import forms
from education.models import EduCenter


class EduCenterEditForm(forms.ModelForm):

    class Meta:
        model = EduCenter
        fields = [
            "name",
            "logo",
        ]
