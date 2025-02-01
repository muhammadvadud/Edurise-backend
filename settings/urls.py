from django.urls import path

from accounts.models import Users
from middlewares.role import IsRole
from .views import ListViewPage, EditViewPage

app_name = "settings"

urlpatterns = [
    path(
        "list/",
        IsRole(ListViewPage.as_view(), roles=[Users.ROLE_CEO]),
        name="list",
    ),
    path(
        "edit/",
        IsRole(EditViewPage.as_view(), roles=[Users.ROLE_CEO]),
        name="edit",
    ),
]
