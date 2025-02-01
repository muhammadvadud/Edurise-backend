from rest_framework import serializers

from registration.models import Registration


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            "first_name",
            "last_name",
            "educenter",
            "course",
            "phone",
            "days",
            "gender",
            "birth_day",
        ]
