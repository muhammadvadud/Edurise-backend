import uuid

import qrcode
from PIL import Image, ImageDraw, ImageFont
from random import randint


class Certificate:

    def __init__(self, image=None):
        if image is None:
            image = "helpers/assets/image.jpg"
        self.image = Image.open(image)
        self.draw = ImageDraw.Draw(self.image)
        self.font = self.get_font(160)

    def get_qr(self, url):
        img = qrcode.make(url)
        img.save("helpers/assets/qr.png")

        return Image.open("helpers/assets/qr.png")

    def get_font(self, size, font=None):

        if font is None:
            font = "helpers/assets/Font-1.ttf"
        return ImageFont.truetype(font, size)

    def write(self, text, x, y):
        fill = (0, 0, 0)
        if self.color is not None:
            fill = self.color

        return self.draw.text((x, y), text, font=self.font, fill=fill)

    def generate(self, FIO, course, complate, color=None):

        cid = "181{}".format(randint(10000, 99999))

        self.color = color

        self.write(FIO, 200, 1070)

        self.color = (119, 221, 4)
        self.font = self.get_font(90)

        self.write(course, 200, 1270)

        self.color = None
        self.font = self.get_font(100)
        self.write(complate, 200, 1380)

        self.color = None
        self.font = self.get_font(100)
        self.write(cid, 2550, 2010)

        self.filename = f"{uuid.uuid4()}.jpg"
        self.filepath = f"web/media/temp/{self.filename}"

        self.image.paste(
            self.get_qr("http://127.0.0.1:8000{}".format(f"/web/media/certificates/{self.filename}")),
            (2330, 150),
        )

        self.image.save(self.filepath)

        return self.filepath, self.filename

    def get_cid(self):
        return "181{}".format(randint(10000, 99999))

    def set_size(self, size: int) -> None:
        self.font = self.get_font(size)

    def generate_v2(self, FIO, course_count: str = "32", color=None):
        """Generate certificates v2

        Args:
            FIO (_type_): first_name and last_name
            course_count (str, optional): courses count. Defaults to "32".
            color (_type_, optional): first text color. Defaults to None.
        """

        """BaseVariables"""
        self.filename = f"img.jpg"
        self.filepath = f"web/media/temp/{self.filename}"

        self.color = color  # set new color

        self.write(FIO, 1080, 950)  # write first_name and last_name
        self.color = None  # set default color

        self.set_size(85)  # set font size

        self.write(course_count, 1310, 1322)
        self.color = "#fff"

        self.set_size(80)  # set font size

        self.write(self.get_cid(), 2880, 2330)

        self.image.paste(
            self.get_qr("https://edusystem.uz{}".format(f"/web/media/certificates/{self.filename}")),
            (2780, 1630),
        )
        self.image.save(self.filepath)
        return self.filepath, self.filename
