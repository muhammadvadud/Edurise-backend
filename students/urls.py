from django.urls import path

from accounts.models import Users
from helpers.roles import Roles
from .views import ListViewPage, CreateViewPage, DeleteViewPage, EditViewPage
from middlewares.role import IsRole

app_name = "students"

urlpatterns = [
    path(
        "list/", IsRole(ListViewPage.as_view(), roles=Roles.main), name="list"
    ),
    path(
        "create/",
        IsRole(CreateViewPage.as_view(), roles=Roles.main),
        name="create",
    ),
    path(
        "delete/<int:pk>/",
        IsRole(DeleteViewPage.as_view(), roles=Roles.main),
        name="delete",
    ),
    path(
        "edit/<int:pk>/",
        IsRole(EditViewPage.as_view(), roles=Roles.main),
        name="edit",
    ),
]
