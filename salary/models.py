from django.db import models
from django.db.models import Sum
from datetime import date, timedelta
from teachers.models import Teachers
from payments.models import Payments


class TeacherSalary(models.Model):
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name="salaries")
    month = models.DateField()  # Oylik hisoblangan oy
    total_income = models.BigIntegerField()  # O'qituvchiga tushgan umumiy summa
    salary_amount = models.BigIntegerField()  # O'qituvchiga ajratilgan foiz

    def __str__(self):
        return f"{self.teacher} - {self.month.strftime('%Y-%m')} - {self.salary_amount} so'm"

    @classmethod
    def calculate_salary(cls, teacher, month):
        """
        O'qituvchining oylik daromadini hisoblaydi va salary maydoniga asoslanib foizni ajratadi.
        """
        # Salary maydonidagi foizni olish
        try:
            percentage = int(teacher.salary)  # Foizni son shaklida olish
        except (ValueError, TypeError):
            percentage = 15  # Agar salary noto‘g‘ri bo‘lsa, default 15% olamiz

        start_date = month.replace(day=1)  # Oyning birinchi kuni
        next_month = start_date.replace(day=28) + timedelta(days=4)  # Keyingi oyga o'tish
        end_date = next_month - timedelta(days=next_month.day)  # Hozirgi oyning oxiri

        # O'qituvchiga tushgan jami summa
        total_income = Payments.objects.filter(
            student__groups__teachers=teacher,
            date__range=(start_date, end_date)
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # O'qituvchiga ajratilgan maoshni hisoblash
        salary_amount = (total_income * percentage) // 100

        # Ma'lumotni saqlash yoki yangilash
        salary_record, created = cls.objects.update_or_create(
            teacher=teacher,
            month=start_date,
            defaults={'total_income': total_income, 'salary_amount': salary_amount}
        )
        return salary_record
