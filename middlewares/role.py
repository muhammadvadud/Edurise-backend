from django.core.exceptions import PermissionDenied
from accounts.models import Users


def CheckRole(user, role=None, roles=[]):
    if user.role == role:
        return True

    for r in roles:
        if user.role == r:
            return True

    return False


# Super Admin uchun middleware
class IsSuperAdmin:
    def __init__(self, response):
        self.response = response

    def __call__(self, request, *args, **kwargs):
        if request.user.role == Users.ROLE_SUPER_ADMIN:
            resource = self.response(request, *args, **kwargs)
            return resource
        else:
            raise PermissionDenied


class IsRole:
    def __init__(self, response, role=None, roles=[]):
        self.role = role
        self.roles = roles
        self.response = response

    def __call__(self, request, *args, **kwargs):
        status = False

        for r in self.roles:
            if request.user.role == r:
                status = True
                break

        if request.user.role == self.role or status:
            resource = self.response(request, *args, **kwargs)
            return resource
        else:
            raise PermissionDenied
