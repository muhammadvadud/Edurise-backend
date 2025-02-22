# Python image ni tanlaymiz
FROM python:3.12-slim

# Ishchi katalogni belgilaymiz
WORKDIR /app
RUN apt-get update && apt-get install -y locales && \
    echo "uz_UZ.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen uz_UZ.UTF-8

# Lokal sozlamalarini o‘rnatish
ENV LANG uz_UZ.UTF-8
ENV LANGUAGE uz_UZ:uz
ENV LC_ALL uz_UZ.UTF-8
# Talablar faylini nusxalaymiz
COPY requirements.txt /app/

# Talablarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha fayllarini nusxalaymiz
COPY . /app/

# Django serverini ishga tushirish uchun buyruq
CMD ["python", "manage.py", "runserver", "0.0.0.0:8008"]