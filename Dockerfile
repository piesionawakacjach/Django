FROM python:3.14-slim
WORKDIR /app

COPY . .

RUN useradd -m appuser
USER appuser

RUN pip install - r requirements.txt

CMD ["python", "-m", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3",  "--access-logfile=-", "--capture-output"]