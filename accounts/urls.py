from django.urls import path
from .views import ProfilePageView, TeacherProfilePageView

app_name = "accounts"

urlpatterns = [
    path("user/student/<int:pk>/", ProfilePageView.as_view(), name="student"),
    path(
        "user/teacher/<int:pk>/",
        TeacherProfilePageView.as_view(),
        name="teacher",
    ),
]
