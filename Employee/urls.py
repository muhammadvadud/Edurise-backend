from django.urls import path
from Employee.views import (
    CreatePageView,
    ListPageView,
    EditPageView,
    DeletePageView,
)

app_name = "Employee"

urlpatterns = [
    path("list/", ListPageView.as_view(), name="list"),
    path("create/", CreatePageView.as_view(), name="create"),
    path("edit/<int:pk>/", EditPageView.as_view(), name="edit"),
    path("delete/<int:pk>/", DeletePageView.as_view(), name="delete"),
]
