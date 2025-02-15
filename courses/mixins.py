from django.core.exceptions import PermissionDenied
from accounts.models import Users  # User modelini import qilish


class CeoRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        print(f"User: {request.user}, Role: {request.user.role}")  # Terminalga chiqarish

        if request.user.role == Users.ROLE_CEO:  # String bilan emas, raqam bilan solishtirish!
            return super().dispatch(request, *args, **kwargs)
        if request.user.role == Users.ROLE_ADMINISTRATOR:  # String bilan emas, raqam bilan solishtirish!
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("Sizda ushbu sahifaga kirish huquqi yo'q.")
