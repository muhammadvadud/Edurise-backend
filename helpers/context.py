from accounts.models import Users
from helpers.helpers import IsRole


def user_context(request):
    user = request.user
    context = {}
    if user.is_authenticated:
        context = {
            "smadmin": IsRole(user, Users.ROLE_SUPER_ADMIN),
            "madmin": IsRole(user, Users.ROLE_ADMIN),
            "ceo": IsRole(user, Users.ROLE_CEO),
            "admin": IsRole(user, Users.ROLE_ADMINISTRATOR),
            "manager": IsRole(user, Users.ROLE_MANGER),
            "casher": IsRole(user, Users.ROLE_CASHER),
            "teacher": IsRole(user, Users.ROLE_TEACHER),
        }
    context["Users"] = Users
    return context
