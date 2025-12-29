FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python src/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--chdir", "src", "--bind", "0.0.0.0:8000", "constructora.wsgi:application"]
