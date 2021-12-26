FROM python:3.10.1-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

# Заглушка на SECRET_KEY, чтобы отработал collectstatic
ARG SECRET_KEY=stub
# Сбор статических файлов
RUN set -e; [ $(ls -A staticfiles) ] || python manage.py collectstatic

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "application", "--bind", "0.0.0.0:8000"]

