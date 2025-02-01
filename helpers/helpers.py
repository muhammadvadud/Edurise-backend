import calendar
from datetime import timedelta, datetime

from django.template import Library
import locale

from accounts.models import Users
from certificate.models import Certificate
from courses.models import Courses
from education.models import EduCenter
from groups.models import Groups, Journal
from payments.models import Payments
from rooms.models import Rooms
from students.models import Students

locale.setlocale(locale.LC_ALL, "uz_UZ.UTF-8")
register = Library()


@register.simple_tag
def toCurrency(number):
    try:
        return f"{'{:,}'.format(int(number))} so'm"
    except:
        return f"0 so'm"


@register.simple_tag
def addMonth(a_date, month):
    date = a_date + timedelta(days=month * 30)
    return date


@register.simple_tag
def getUserRole(user_number):
    return Users.ROLES[user_number - 1][1]


@register.filter
def isParrentFilial(user):
    if user.educenter.parent is None:
        return True
    else:
        return False


@register.simple_tag
def IsRole(user, *args, is_all=False):
    if is_all:
        return True

    for role in args:
        if user.role == role:
            return True
    return False


@register.simple_tag
def ToList(*args):
    return args


@register.simple_tag
def JournalCheck(group, student, month, day, isDisabled=False):
    today = datetime.now()

    journal = Journal.objects.filter(group_id=group, student_id=student)

    s = ""

    if isDisabled:
        s = "check-disabled"

    if not journal.exists():
        return s

    data = journal.first()
    j = data.data

    status = s
    if month in j:
        days = j[month]
        if str(day) in days:
            status = "check-not-active"
    return status


def getDays(year, month, stamp):
    num_days = calendar.monthrange(year, month)[1]

    days = []
    for day in range(1, num_days + 1):
        wday = calendar.weekday(year, month, day) + 1
        if wday in [1, 3, 5] and stamp == 1:
            days.append(day)
        elif wday in [2, 4, 6] and stamp == 0:
            days.append(day)
    return days


@register.simple_tag
def getPaymentMoney(group, student, month):
    today = datetime.now()
    journal = Journal.objects.filter(group_id=group, student_id=student)
    group = Groups.objects.get(id=group)
    if not journal.exists():
        return 0

    data = journal.first()
    j = data.data

    if month in j:
        days = j[month]
        return toCurrency(
            len(days)
            * (
                int(group.price.replace(" ", ""))
                / len(
                    getDays(
                        today.year,
                        getMonthNumber(month),
                        1 if group.days == Groups.ODD_DAYS else 0,
                    )
                )
            )
        )

    return 0


@register.filter
def isGroupUser(group, user):
    return Groups.objects.get(id=group).users.filter(id=user).exists()


def getMonthNumber(name):
    months = [
        "Yan",
        "Fev",
        "Mar",
        "Apr",
        "May",
        "Iyn",
        "Iyl",
        "Avg",
        "Sen",
        "Okt",
        "Noy",
        "Dek",
    ]
    return months.index(name) + 1


@register.filter
def getEduCenter(id):
    students = Students.objects.filter(educenter_id=id).count()
    teachers = Users.objects.filter(
        educenter_id=id, role=Users.ROLE_TEACHER
    ).count()
    rooms = Rooms.objects.filter(educenter_id=id).count()
    courses = Courses.objects.filter(educenter_id=id).count()
    filials = EduCenter.objects.filter(parent=id).count()

    context = {
        "students": students,
        "teachers": teachers,
        "rooms": rooms,
        "courses": courses,
        "filials": filials,
    }

    return context


@register.filter
def isUserCertificate(course, student):
    return not Certificate.objects.filter(
        course_id=course, student_id=student
    ).exists()


@register.filter
def userCertificate(course, student):
    return Certificate.objects.filter(
        course_id=course, student_id=student
    ).first()


@register.filter
def isDebt(group, student):
    res = Payments.objects.filter(
        student=student,
        group_id=group.id,
        educenter=student.educenter,
        date__month=datetime.now().month,
    ).exists()
    return not res
