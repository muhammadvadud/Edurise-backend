from django.urls import path
from helpers.roles import Roles
from .views import ListViewPage, CreateViewPage, delete_certificate
from middlewares.role import IsRole

app_name = "fast_certificate"

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
        "delete/<int:certificate_id>/",
        IsRole(delete_certificate, roles=Roles.main),
        name="delete",
    ),

]
