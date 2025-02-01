from django.urls import path
from .views import SendMessage, RegistrationAPIView

app_name = "api"

urlpatterns = [
    path("send-message/", SendMessage.as_view(), name="send_message"),
    path(
        "registration/<str:token>/",
        RegistrationAPIView.as_view(),
        name="registration",
    ),
]
