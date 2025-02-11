FROM python:3.12

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh  # Skriptni bajarish huquqini berish