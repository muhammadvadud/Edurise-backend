from django.urls import path

from accounts.models import Users
from .views import ListViewPage, CreateViewPage, DeleteViewPage, EditViewPage
from middlewares.role import IsRole

app_name = "education"

urlpatterns = [
    path(
        "list/",
        IsRole(ListViewPage.as_view(), roles=[Users.ROLE_CEO]),
        name="list",
    ),
    path(
        "create/",
        IsRole(CreateViewPage.as_view(), roles=[Users.ROLE_CEO]),
        name="create",
    ),
    path(
        "delete/<int:pk>/",
        IsRole(DeleteViewPage.as_view(), roles=[Users.ROLE_CEO]),
        name="delete",
    ),
    path(
        "edit/<int:pk>/",
        IsRole(EditViewPage.as_view(), roles=[Users.ROLE_CEO]),
        name="edit",
    ),
]
