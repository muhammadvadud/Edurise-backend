from django.core.exceptions import PermissionDenied


class Mixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.educenter.parent is None:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied
