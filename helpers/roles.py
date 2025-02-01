from accounts.models import Users


class Roles:
    main = [
        Users.ROLE_CEO,
        Users.ROLE_SUPER_ADMIN,
        Users.ROLE_TEACHER,
        Users.ROLE_CASHER,
        Users.ROLE_MANGER,
        Users.ROLE_ADMINISTRATOR,
    ]
    ceo = [Users.ROLE_CEO]
