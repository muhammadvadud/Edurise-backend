from django.urls import path

from .views import (
    ListViewPage,
    CreateViewPage,
    DeleteViewPage,
    EditViewPage,
    AddStudentViewPage,
    DetailPageView,
    JournalPageView,
    RemoveStudentViewPage,
    StudentDebtViewPage,
    AddGroupStudent,
)

app_name = "groups"

urlpatterns = [
    path("list/", ListViewPage.as_view(), name="list"),
    path(
        "addStudent/<int:pk>/", AddStudentViewPage.as_view(), name="addStudent"
    ),
    path(
        "addGroupStudent/<int:pk>/",
        AddGroupStudent.as_view(),
        name="AddGroupStudent",
    ),
    path(
        "removeStudent/<int:group>/<int:user>/",
        RemoveStudentViewPage.as_view(),
        name="removeStudent",
    ),
    path(
        "studentDebt/<int:group>/<int:user>/",
        StudentDebtViewPage.as_view(),
        name="studentDebt",
    ),
    path("create/", CreateViewPage.as_view(), name="create"),
    path("delete/<int:pk>/", DeleteViewPage.as_view(), name="delete"),
    path("edit/<int:pk>/", EditViewPage.as_view(), name="edit"),
    path("detail/<int:pk>/", DetailPageView.as_view(), name="detail"),
    path("journal/", JournalPageView.as_view(), name="journal"),
]
