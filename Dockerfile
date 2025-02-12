FROM python:3.12

# Lokalizatsiya uchun kerakli paketlarni o‘rnatish
RUN apt-get update && apt-get install -y locales && \
    echo "uz_UZ.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen uz_UZ.UTF-8

# Lokal sozlamalarini o‘rnatish
ENV LANG uz_UZ.UTF-8
ENV LANGUAGE uz_UZ:uz
ENV LC_ALL uz_UZ.UTF-8

# Ishchi katalogni o‘rnatish
WORKDIR /app

# Kerakli fayllarni nusxalash
COPY . .

# Python kutubxonalarini o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Django loyihasini ishga tushirish
CMD ["gunicorn", "--bind", "0.0.0.0:8008", "app.wsgi:application"]
