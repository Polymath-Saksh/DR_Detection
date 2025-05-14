FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
ENV DJANGO_SETTINGS_MODULE=DR_Detection.settings \
    PYTHONUNBUFFERED=1
CMD ["gunicorn", "DR_Detection.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]