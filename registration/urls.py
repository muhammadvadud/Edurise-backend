from django.urls import path

from accounts.models import Users
from helpers.roles import Roles
from .api import CreateApiView
from .views import ListViewPage, CreateViewPage, DeleteViewPage, EditViewPage
from middlewares.role import IsRole

app_name = "registration"

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

api_urlpatterns = [
    path("api/create/", CreateApiView.as_view()),
]

urlpatterns += api_urlpatterns
