from django.urls import path
from .views import ListViewPage, CreateViewPage, DeleteViewPage, EditViewPage

app_name = "courses"

urlpatterns = [
    path("list/", ListViewPage.as_view(), name="list"),
    path("create/", CreateViewPage.as_view(), name="create"),
    path("delete/<int:pk>/", DeleteViewPage.as_view(), name="delete"),
    path("edit/<int:pk>/", EditViewPage.as_view(), name="edit"),
]
