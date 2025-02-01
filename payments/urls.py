from django.urls import path

from payments.views import PayViewPage, PaymentViewPage, ListViewPage

app_name = "payments"

urlpatterns = [
    path("list/", ListViewPage.as_view(), name="list"),
    path("pay/<int:group>/<int:student>", PayViewPage.as_view(), name="pay"),
    path("payment/", PaymentViewPage.as_view(), name="payment"),
]
