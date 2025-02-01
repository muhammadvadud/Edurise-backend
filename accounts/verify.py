from .models import Users
from django.contrib.auth.backends import ModelBackend


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(phone=username)
        except:
            return None
        else:
            if user.check_password(password):
                return user
        return None
