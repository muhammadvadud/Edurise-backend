import base64

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.views import APIView

from education.models import EduCenter
from registration.models import Registration
from .serializers import MessageSerializer, RegistrationSerializer
from students.models import Students
from helpers.ucell import Ucell


class SendMessage(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ser = MessageSerializer(data=request.data)

        if ser.is_valid():
            message = ser.data.get("message")
            user = ser.data.get("user")
            student = get_object_or_404(Students, id=user)
            phone = (
                str(student.phone)
                .replace(" ", "")
                .replace("-", "")
                .replace("+", "")
            )
            res = Ucell.sendMessage(phone, message)
            return Response(res)

        return Response({"response": "fields.not.confirmed", "success": False})


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def get_id(self, token):
        return str(base64.b64decode(token).decode("utf-8")).split("=")[1]

    def get_educenter(self, token):
        id = self.get_id(token)
        return get_object_or_404(EduCenter, id=id)

    def get(self, request, token):
        try:
            educenter = self.get_educenter(token)
        except:
            return Response(
                {"success": False, "message": "educenter.not.found"},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

        courses = EduCenter.objects.get(
            id=self.get_id(token)
        ).courses_set.all()

        response = {
            "name": educenter.name,
            "logo": request.build_absolute_uri(educenter.logo.url),
            "courses": courses.values(),
        }
        return Response(response)

    def post(self, request, token):
        educenter = self.get_educenter(token)

        ser = RegistrationSerializer(data=request.data)

        if not ser.is_valid():
            return Response(
                {"response": "fields.not.confirmed"}, status=HTTP_403_FORBIDDEN
            )

        Registration.objects.create(
            first_name=ser.data.get("first_name"),
            last_name=ser.data.get("last_name"),
            course_id=ser.data.get("course"),
            phone=ser.data.get("phone"),
            days=ser.data.get("days"),
            gender=ser.data.get("gender"),
            birth_day=ser.data.get("birth_day"),
            educenter_id=self.get_id(token),
        )
        return Response({"response": "success"})
