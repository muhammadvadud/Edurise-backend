from rest_framework import serializers

from registration.models import Registration


class MessageSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    message = serializers.CharField(max_length=255)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            "first_name",
            "last_name",
            "course",
            "phone",
            "days",
            "gender",
            "birth_day",
        ]
