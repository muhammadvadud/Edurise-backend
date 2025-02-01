from django.urls import path
from .views import (
    ListViewPage,
    CreateViewPage,
    DeleteViewPage,
    EditViewPage,
    EduLogin,
)
from middlewares.role import IsSuperAdmin

app_name = "adm"

urlpatterns = [
    path("edulist/", IsSuperAdmin(ListViewPage.as_view()), name="edulist"),
    path(
        "educreate/", IsSuperAdmin(CreateViewPage.as_view()), name="educreate"
    ),
    path(
        "delete/<int:pk>/",
        IsSuperAdmin(DeleteViewPage.as_view()),
        name="edudelete",
    ),
    path(
        "edit/<int:pk>/", IsSuperAdmin(EditViewPage.as_view()), name="eduedit"
    ),
    path(
        "edu-login/<int:pk>/",
        IsSuperAdmin(EduLogin.as_view()),
        name="edulogin",
    ),
]
