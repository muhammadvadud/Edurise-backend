# from rest_framework.generics import Api
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from .models import Registration
from .serializers import CreateSerializer


class CreateApiView(APIView):
    serializer_class = CreateSerializer

    def post(self, request):
        ser = CreateSerializer(data=request.data)

        if not ser.is_valid():
            return Response(
                {
                    "success": False,
                    "message": "fields.not.confirmed",
                    "errors": ser.errors,
                },
                status=HTTP_403_FORBIDDEN,
            )
        try:
            ser.save()
            return Response(
                {"success": True, "message": "registration.create"}
            )
        except Exception as e:
            return Response({"success": False, "message": "server.error"})
