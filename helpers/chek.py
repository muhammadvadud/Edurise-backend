import os
import random
import qrcode
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def generate_receipt(student_name, group_name, payment_type, amount, educenter_name, date, course_name, payment_id,
                     status):
    """PDF chek yaratish funksiyasi"""

    random_id = random.randint(10000000, 99999999)

    # **Chekni MEDIA_ROOT ichiga saqlash**
    cheks_folder = os.path.join(settings.MEDIA_ROOT, "chek")
    os.makedirs(cheks_folder, exist_ok=True)  # Agar papka bo'lmasa, yaratadi

    file_name = f"{random_id}.pdf"
    file_path = os.path.join(cheks_folder, file_name)

    qr_data = f"https://edurise.uz/media/chek/{random_id}"
    qr = qrcode.make(qr_data)
    qr_file = os.path.join(cheks_folder, f"qr_{random_id}.png")
    qr.save(qr_file)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    title_font_size = 23
    value_font_size = 20

    # **O'quv markaz**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 50, "O‘quv Markaz:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 50, f"{educenter_name}")

    # **Student name**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 90, "O'quvchining FISH:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 90, f"{student_name}")

    # **Cours**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 130, "Kurs:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 130, f"{course_name}")

    # **Group**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 170, "Guruh:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 170, f"{group_name}")

    # **To‘lov id**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 210, "To‘lov raqami:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 210, f"{payment_id}")

    # **To‘lov miqdori**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 250, "To‘lov miqdori:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 250, f"{amount} so‘m")

    # **To‘lov turi**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 290, "To‘lov turi:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 290, f"{payment_type}")

    # **Chek Random id**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 330, "Chek raqami:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 330, f"{random_id}")

    # **To'landi**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 370, "To‘landi:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 370, f"{amount}")

    # **To‘lov sanasi**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 410, "To‘lov sanasi:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 410, f"{date}")

    # **Holati**
    c.setFont("Helvetica", title_font_size)
    c.setFillColor(colors.gray)
    c.drawRightString(240, height - 450, "Holati:")
    c.setFont("Helvetica", value_font_size)
    c.setFillColor(colors.black)
    c.drawString(250, height - 450, f"{status}")

    c.drawImage(qr_file, width - 470, height - 810, width=350, height=350)

    c.save()
    os.remove(qr_file)

    # Faqat media ichidagi yo‘lni qaytarish

    return file_path
